"""Collector guard tests with the fake PayPal and fake LLM providers."""
from datetime import datetime, timezone
from uuid import uuid4

import app.agents.base as agent_base
from app.agents.base import AgentContext
from app.agents.collector import handle
from app.ledger import find, seal
from app.models import CollectorPlan, Event


def _event(
    type_: str,
    invoice: str,
    days: int,
    amount: int = 60000,
    history: tuple[int, int] = (3, 0),
    average: int | None = None,
) -> Event:
    data = {
        "type": type_,
        "subject_id": invoice,
        "invoice": {
            "invoice_id": invoice,
            "amount_cents": amount,
            "currency": "USD",
            "days_overdue": days,
        },
        "client_history": {"total_invoices": history[0], "late_invoices": history[1]},
    }
    if average is not None:
        data["average_invoice_cents"] = average
    return Event(
        id=str(uuid4()),
        type=type_,
        source="scheduler",
        subject_id=invoice,
        data=data,
        verified=True,
        received_at=datetime.now(timezone.utc),
    )


def _reminder_decisions(invoice: str) -> list:
    return [
        entry for entry in find(kind="decision", subject_id=invoice)
        if (entry.payload or {}).get("agent") == "collector"
        and (entry.payload or {}).get("tool") == "send_invoice_reminder"
    ]


def test_overdue_invoice_sends_a_safe_reminder() -> None:
    plan = handle(_event("invoice.overdue", "INV-C1", 5, amount=60000), AgentContext("collector"))

    assert (plan.risk, plan.tone, plan.next_action) == ("low", "friendly", "remind")
    assert "INV-C1" in plan.reminder_note
    assert "600.00" in plan.reminder_note

    [decision] = _reminder_decisions("INV-C1")
    assert decision.payload["outcome"] == "allow"
    assert decision.payload["args"]["invoice_id"] == "INV-C1"
    assert decision.payload["args"]["note"] == plan.reminder_note


def test_reminder_count_moves_from_firm_to_escalation() -> None:
    event = _event("invoice.overdue", "INV-C2", 12, amount=15000)

    first = handle(event, AgentContext("collector"))
    second = handle(event, AgentContext("collector"))
    third = handle(event, AgentContext("collector"))

    assert (first.tone, first.next_action) == ("friendly", "remind")
    assert (second.tone, second.next_action) == ("firm", "remind")
    assert (third.risk, third.tone, third.next_action) == ("high", "final", "escalate")
    assert len(_reminder_decisions("INV-C2")) == 2


def test_not_due_invoice_waits_without_a_tool_call() -> None:
    plan = handle(_event("invoice.sent", "INV-C3", 0, amount=30000), AgentContext("collector"))

    assert (plan.risk, plan.tone, plan.next_action) == ("low", "friendly", "wait")
    assert "not past due" in plan.reminder_note
    assert _reminder_decisions("INV-C3") == []


def test_paid_invoice_waits_without_a_tool_call() -> None:
    seal(
        "event",
        "INV-C4",
        "payment captured",
        {
            "type": "payment.captured",
            "verified": True,
            "invoice_id": "INV-C4",
            "amount_cents": 7500,
            "currency": "USD",
        },
    )

    plan = handle(_event("invoice.overdue", "INV-C4", 30, amount=7500), AgentContext("collector"))

    assert (plan.risk, plan.tone, plan.next_action) == ("low", "friendly", "wait")
    assert "already recorded" in plan.reminder_note
    assert _reminder_decisions("INV-C4") == []


def test_llm_cannot_override_risk_tone_or_action(monkeypatch) -> None:
    note = "Invoice INV-C5 for $120.00 USD is now 25 days past due. Please pay now or reply with a date."
    monkeypatch.setattr(
        agent_base,
        "llm_complete",
        lambda system, user, schema: CollectorPlan(
            invoice_id="INV-C5",
            risk="low",
            days_overdue=0,
            tone="friendly",
            reminder_note=note,
            next_action="wait",
        ),
    )

    plan = handle(_event("invoice.overdue", "INV-C5", 25, amount=12000), AgentContext("collector"))

    assert (plan.risk, plan.tone, plan.next_action) == ("high", "firm", "remind")
    assert plan.reminder_note == note
    assert _reminder_decisions("INV-C5")[0].payload["args"]["note"] == note


def test_llm_threat_is_replaced_with_safe_note(monkeypatch) -> None:
    monkeypatch.setattr(
        agent_base,
        "llm_complete",
        lambda system, user, schema: CollectorPlan(
            invoice_id="INV-C6",
            risk="high",
            days_overdue=20,
            tone="final",
            reminder_note="Invoice INV-C6 for $600.00 USD is overdue. Pay now or we will sue you.",
            next_action="remind",
        ),
    )

    plan = handle(_event("invoice.overdue", "INV-C6", 20), AgentContext("collector"))

    assert "sue" not in plan.reminder_note.lower()
    assert "INV-C6" in plan.reminder_note and "600.00" in plan.reminder_note
    assert _reminder_decisions("INV-C6")[0].payload["args"]["note"] == plan.reminder_note
