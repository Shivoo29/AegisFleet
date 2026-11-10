"""Agent-driven schedule. Agents plan their own future actions (a follow-up reminder, a tracking check,
a deadline guard); the seller can move or cancel them on the Timeline; a runner executes them when due.

A plan is only an intention: when it fires it goes through gateway.call like any other action, so a
plan the gateway would refuse (cap reached, kill switch on) is blocked, not run. Every plan, move,
cancel and result is sealed in the ledger.
"""
import json
import logging
import uuid
from datetime import datetime, timezone

from app.db import conn
from app.ledger import seal

log = logging.getLogger("aegis.plans")
COLUMNS = "id, agent, tool, args, reason, title, subject_id, due_at, status, outcome, created_at, updated_at"


def _rows(sql: str, args: tuple = ()) -> list:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(sql, args)
            rows = cur.fetchall() if cur.description else []
        c.commit()
    return rows


def add(agent: str, tool: str, args: dict, reason: str, title: str, due_at: datetime) -> str:
    subject = str(args.get("subject_id") or args.get("invoice_id") or args.get("dispute_id") or "unknown")
    pid = f"plan_{uuid.uuid4().hex[:8]}"
    _rows("INSERT INTO plans (id, agent, tool, args, reason, title, subject_id, due_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
          (pid, agent, tool, json.dumps(args), reason, title, subject, due_at))
    seal(kind="note", subject_id=subject, summary=f"{agent} planned: {title} ({due_at:%d %b %H:%M} UTC)",
         payload={"plan_id": pid, "agent": agent, "tool": tool, "due_at": due_at.isoformat(), "title": title})
    return pid


def listing() -> list:
    return _rows(f"SELECT {COLUMNS} FROM plans ORDER BY due_at")


def move(plan_id: str, due_at: datetime, by: str) -> dict:
    old = _rows("SELECT due_at FROM plans WHERE id=%s AND status='planned'", (plan_id,))
    rows = _rows(f"UPDATE plans SET due_at=%s, updated_at=now() WHERE id=%s AND status='planned' RETURNING {COLUMNS}",
                 (due_at, plan_id))
    if not old or not rows:
        raise KeyError(plan_id)
    p = {**rows[0], "was": old[0]["due_at"]}
    seal(kind="note", subject_id=p["subject_id"],
         summary=f"{by} moved {p['agent']}'s plan '{p['title']}' to {due_at:%d %b %H:%M} UTC",
         payload={"plan_id": plan_id, "by": by, "from": p["was"].isoformat(), "to": due_at.isoformat()})
    return p


def cancel(plan_id: str, by: str, why: str = "") -> None:
    rows = _rows("UPDATE plans SET status='cancelled', updated_at=now() WHERE id=%s AND status='planned' "
                 "RETURNING subject_id, agent, title", (plan_id,))
    if not rows:
        raise KeyError(plan_id)
    p = rows[0]
    seal(kind="note", subject_id=p["subject_id"], summary=f"{by} cancelled {p['agent']}'s plan '{p['title']}'",
         payload={"plan_id": plan_id, "by": by, "why": why})


def cancel_for(subject_id: str, tools: set[str], why: str) -> None:
    """An agent re-plans when facts change, e.g. invoice paid -> drop the follow-up reminders."""
    for p in _rows("SELECT id FROM plans WHERE subject_id=%s AND status='planned' AND tool = ANY(%s)",
                   (subject_id, list(tools))):
        cancel(p["id"], "aegisfleet", why)


def run_due() -> int:
    """Claim and run every plan that is due. Returns how many ran."""
    from app.gateway import gateway
    claimed = _rows(f"UPDATE plans SET status='running', updated_at=now() WHERE id IN "
                    f"(SELECT id FROM plans WHERE status='planned' AND due_at <= now() ORDER BY due_at "
                    f"FOR UPDATE SKIP LOCKED) RETURNING {COLUMNS}")
    for p in sorted(claimed, key=lambda r: r["due_at"]):  # UPDATE ... RETURNING has no order
        try:
            d = gateway.call(p["agent"], p["tool"], p["args"], f"planned: {p['reason']}")
            status = {"allow": "done", "hold": "held", "deny": "blocked"}[d.outcome]
            outcome = {"outcome": d.outcome, "reason": d.reason, "ledger_entry": d.ledger_entry_id,
                       "approval_id": d.approval_id}
        except Exception as e:  # noqa: BLE001 — a broken plan must not stop the others
            log.exception("plan %s failed", p["id"])
            status, outcome = "blocked", {"outcome": "error", "reason": str(e)}
        _rows("UPDATE plans SET status=%s, outcome=%s, updated_at=now() WHERE id=%s",
              (status, json.dumps(outcome), p["id"]))
    return len(claimed)


def now() -> datetime:
    return datetime.now(timezone.utc)
