"""Agent-driven schedule: agents plan, facts re-plan, the seller moves, the runner goes through the gateway."""
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app import plans
from app.events import route, store_event
from app.models import Event


def _fire(type_: str, data: dict, verified: bool = True) -> None:
    ev = Event(id=f"t_{uuid4().hex[:8]}", type=type_, source="scheduler", subject_id=data["subject_id"],
               data=data, verified=verified, received_at=datetime.now(timezone.utc))
    store_event(ev)
    route(ev)


def _overdue() -> None:
    due = (datetime.now(timezone.utc) - timedelta(days=9)).isoformat()
    _fire("invoice.overdue", {"subject_id": "INV-0006", "invoice_id": "INV-0006", "amount_cents": 18500,
                              "currency": "USD", "due_date": due,
                              "client_history": {"total_invoices": 4, "late_invoices": 1}})


def test_collector_plans_follow_ups_and_payment_cancels_them() -> None:
    _overdue()
    mine = [p for p in plans.listing() if p["agent"] == "collector"]
    assert [p["title"] for p in mine] == ["Follow-up reminder (firmer)", "Final notice before escalation"]
    assert all(p["status"] == "planned" for p in mine)
    _fire("invoice.paid", {"subject_id": "INV-0006", "invoice_id": "INV-0006", "amount_cents": 18500})
    assert {p["status"] for p in plans.listing() if p["agent"] == "collector"} == {"cancelled"}


def test_seller_moves_a_plan_and_runner_respects_the_cap() -> None:
    _overdue()  # reminder #1 sent now (cap is 2 per week)
    follow_up, final = [p for p in plans.listing() if p["agent"] == "collector"]
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    moved = plans.move(follow_up["id"], past, "dev")
    assert moved["due_at"] <= datetime.now(timezone.utc)
    plans.move(final["id"], past + timedelta(seconds=30), "dev")  # seller pulls the final notice into this week
    assert plans.run_due() == 2
    by_title = {p["title"]: p for p in plans.listing()}
    assert by_title["Follow-up reminder (firmer)"]["status"] == "done"
    blocked = by_title["Final notice before escalation"]
    assert blocked["status"] == "blocked" and "cap" in blocked["outcome"]["reason"]


def test_cancel_is_sealed() -> None:
    _overdue()
    p = plans.listing()[0]
    plans.cancel(p["id"], "dev")
    from app.ledger import find
    assert any("cancelled collector's plan" in e.summary for e in find(limit=50))
