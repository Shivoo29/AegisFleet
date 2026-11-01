"""Gateway (M6). Single chokepoint for every agent tool call."""
import json
import uuid

from app.db import conn
from app.ledger import seal
from app.models import Decision
from app.gateway import rules


def _seal_decision(outcome: str, reason: str, agent: str, tool: str, args: dict, approval_id: str | None = None, result: dict | None = None) -> Decision:
    entry = seal(
        kind="decision",
        subject_id=args.get("subject_id") or args.get("invoice_id") or args.get("dispute_id") or "unknown",
        summary=f"{agent}.{tool} -> {outcome}",
        payload={
            "agent": agent,
            "tool": tool,
            "args": args,
            "outcome": outcome,
            "reason": reason,
            "approval_id": approval_id,
            "result": result,
        },
    )
    return Decision(
        outcome=outcome,
        reason=reason,
        approval_id=approval_id,
        result=result,
        ledger_entry_id=entry.id,
    )


def call(agent: str, tool: str, args: dict, reason: str) -> Decision:
    """Order: kill switch → agent enabled → allowlist → validate → caps → approval rule → execute → seal."""
    # 1. kill switch
    if rules.kill_switch_active():
        return _seal_decision("deny", "kill switch active", agent, tool, args)

    # 2. agent enabled
    if not rules.agent_enabled(agent):
        return _seal_decision("deny", f"agent {agent} not enabled", agent, tool, args)

    # 3. allowlist
    if not rules.is_allowed(agent, tool):
        return _seal_decision("deny", f"tool {tool} not allowed for agent {agent}", agent, tool, args)

    # 4. arg validation
    err = rules.validate(agent, tool, args)
    if err:
        return _seal_decision("deny", f"validation failed: {err}", agent, tool, args)

    # 5. caps (FOR UPDATE) — TODO(SKJ): implement budget row check + increment
    # TODO(SKJ): caps FOR UPDATE

    # 6. approval rule
    if rules.needs_approval(agent, tool, args):
        approval_id = f"apr_{uuid.uuid4().hex[:8]}"
        amount_cents = args.get("amount_cents")
        currency = args.get("currency")
        with conn() as c:
            with c.cursor() as cur:
                cur.execute(
                    "INSERT INTO approvals (id, agent, tool, args, reason, summary, amount_cents, currency, status) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'pending')",
                    (
                        approval_id, agent, tool,
                        json.dumps(args), reason,
                        f"{agent} wants to {tool}", amount_cents, currency,
                    ),
                )
            c.commit()
        return _seal_decision(
            "hold",
            "requires human approval",
            agent, tool, args,
            approval_id=approval_id,
            result=None,
        )

    # 7. execute
    from app.paypal.client import get_client
    client = get_client()
    try:
        result = getattr(client, tool)(args)
    except NotImplementedError:
        return _seal_decision("deny", f"{tool} not implemented at M0", agent, tool, args)
    except Exception as e:  # noqa: BLE001
        return _seal_decision("deny", f"execution failed: {e}", agent, tool, args)

    # 8. seal
    return _seal_decision("allow", reason, agent, tool, args, result=result)


def approve(approval_id: str, by: str) -> None:
    raise NotImplementedError("set at M0")


def reject(approval_id: str, by: str) -> None:
    raise NotImplementedError("set at M0")