"""Sentinel (P0). Stub — A owns the impl; contract frozen here."""
from app.agents.base import AgentContext
from app.models import Event, SentinelVerdict


def handle(event: Event, ctx: AgentContext) -> SentinelVerdict:
    # TODO(A): extract text/ids, ledger check, LLM, then guard.
    ctx.log("note", f"sentinel: checking invoice {event.subject_id}")
    return SentinelVerdict(
        verdict="unsure",
        confidence=0.0,
        matched_payment_entry_id=None,
        red_flags=[],
        explanation="",
    )