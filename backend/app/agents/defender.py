"""Defender (P0). Stub — A owns the impl; contract frozen here."""
from app.agents.base import AgentContext
from app.models import EvidencePack, Event


def handle(event: Event, ctx: AgentContext) -> EvidencePack:
    # TODO(A): implement Defender logic — gather facts, checklist, LLM, recommend.
    return EvidencePack(
        dispute_id=event.subject_id,
        reason="TODO(A)",
        classification="unclear",
        confidence=0.0,
        checklist={},
        facts=[],
        note_to_paypal="",
        recommended_action="provide_evidence",
    )