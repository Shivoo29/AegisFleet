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

    # 5. caps
    if not _take_budget(agent, tool, args):
        return _seal_decision("deny", f"cap reached for {tool} on this subject this week", agent, tool, args)

    # 6. approval rule
    if rules.needs_approval(agent, tool, args):
        approval_id = f"apr_{uuid.uuid4().hex[:8]}"
        with conn() as c:
            with c.cursor() as cur:
                cur.execute(
                    "INSERT INTO approvals (id, agent, tool, args, reason, summary, amount_cents, currency, status) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'pending')",
                    (approval_id, agent, tool, json.dumps(args), reason,
                     f"{agent} wants to {tool}", args.get("amount_cents"), args.get("currency")),
                )
            c.commit()
        return _seal_decision("hold", "requires human approval", agent, tool, args, approval_id=approval_id)

    # 7-8. execute + seal
    return _execute(agent, tool, args, reason)


def _subject(args: dict) -> str:
    return str(args.get("subject_id") or args.get("invoice_id") or args.get("dispute_id") or "unknown")


def _take_budget(agent: str, tool: str, args: dict) -> bool:
    """Count one use against CAPS for this subject in the current week. False if over cap."""
    cap = rules.CAPS.get((agent, tool))
    if cap is None:
        return True
    # ponytail: calendar-week window (Monday start), not rolling 7 days; fine for a demo cap.
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "INSERT INTO budgets (agent, tool, subject_id, window_start) "
                "VALUES (%s,%s,%s,date_trunc('week', now())::date) ON CONFLICT DO NOTHING",
                (agent, tool, _subject(args)))
            cur.execute(
                "SELECT count FROM budgets WHERE agent=%s AND tool=%s AND subject_id=%s "
                "AND window_start=date_trunc('week', now())::date FOR UPDATE",
                (agent, tool, _subject(args)))
            if cur.fetchone()["count"] >= cap:
                return False
            cur.execute(
                "UPDATE budgets SET count=count+1, amount_cents=amount_cents+%s WHERE agent=%s AND tool=%s "
                "AND subject_id=%s AND window_start=date_trunc('week', now())::date",
                (args.get("amount_cents") or 0, agent, tool, _subject(args)))
        c.commit()
    return True


def _execute(agent: str, tool: str, args: dict, reason: str, approval_id: str | None = None) -> Decision:
    from app.paypal.client import get_client
    from app.paypal.fake import FakePayPal
    simulated = rules.is_simulated(args)
    client = FakePayPal() if simulated else get_client()
    try:
        result = getattr(client, tool)(args)
    except NotImplementedError:
        return _seal_decision("deny", f"{tool} not implemented yet", agent, tool, args, approval_id)
    except Exception as e:  # noqa: BLE001
        return _seal_decision("deny", f"execution failed: {e}", agent, tool, args, approval_id)
    if simulated:
        result = {**(result or {}), "simulated": True}
        reason = f"{reason} (simulated PayPal: demo record)"
    return _seal_decision("allow", reason, agent, tool, args, approval_id, result=result)


def _decide(approval_id: str, by: str, status: str, note: str) -> dict:
    """Flip a pending approval to status; raises KeyError if missing or already decided."""
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "UPDATE approvals SET status=%s, decided_by=%s, decided_at=now() "
                "WHERE id=%s AND status='pending' RETURNING agent, tool, args, reason",
                (status, by, approval_id))
            row = cur.fetchone()
        c.commit()
    if row is None:
        raise KeyError(approval_id)
    seal(kind="approval", subject_id=_subject(row["args"]),
         summary=f"{by} {status} {row['agent']}.{row['tool']}",
         payload={"approval_id": approval_id, "status": status, "by": by, "note": note})
    return row


def approve(approval_id: str, by: str, note: str = "") -> Decision:
    """Human said yes: run the stored call. Kill switch still applies; approval rule is skipped."""
    row = _decide(approval_id, by, "approved", note)
    agent, tool, args = row["agent"], row["tool"], row["args"]
    if rules.kill_switch_active():
        return _seal_decision("deny", "kill switch active", agent, tool, args, approval_id)
    return _execute(agent, tool, args, row["reason"], approval_id)


def reject(approval_id: str, by: str, note: str = "") -> None:
    _decide(approval_id, by, "rejected", note)
