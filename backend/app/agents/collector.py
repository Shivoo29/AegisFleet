"""Collector (P1). Stub — A owns the impl; contract frozen here."""
from app.agents.base import AgentContext
from app.models import CollectorPlan, Event


def handle(event: Event, ctx: AgentContext) -> CollectorPlan:
    # TODO(A): implement Collector logic — risk score, tone, LLM, remind.
    return CollectorPlan(
        invoice_id=event.subject_id,
        risk="med",
        days_overdue=0,
        tone="friendly",
        reminder_note="TODO(A)",
        next_action="remind",
    )