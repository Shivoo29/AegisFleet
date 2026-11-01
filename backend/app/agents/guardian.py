"""Guardian (P1). Stub — A owns the impl; contract frozen here."""
from app.agents.base import AgentContext
from app.models import Event, HealthReport


def handle(event: Event, ctx: AgentContext) -> HealthReport:
    # TODO(A): implement Guardian logic — tracking, health score, recs.
    return HealthReport(
        score=100,
        factors=[],
        recommendations=["TODO(A)"],
        appeal_pack=None,
    )