"""Defender guard tests with the fake LLM provider."""
from datetime import datetime, timezone
from uuid import uuid4

import app.agents.base as agent_base
from app.agents.base import AgentContext
from app.agents.defender import handle
from app.db import conn
from app.ledger import seal
from app.models import EvidencePack, Event, Fact


def _event(dispute_id: str, invoice: str, reason: str, amount: int = 60000) -> Event:
    return Event(
        id=str(uuid4()),
        type="dispute.created",
        source="paypal",
        subject_id=dispute_id,
        data={
            "type": "dispute.created",
            "subject_id": dispute_id,
            "dispute": {
                "dispute_id": dispute_id,
                "reason": reason,
                "status": "OPEN",
                "amount": {"value": f"{amount / 100:.2f}", "currency_code": "USD"},
                "seller_transactions": [{"transaction_id": "TXN-T", "invoice_id": invoice}],
            },
        },
        verified=True,
        received_at=datetime.now(timezone.utc),
    )


def _payment(invoice: str, verified: bool = True) -> int:
    entry = seal(
        "event",
        invoice,
        "payment captured",
        {
            "type": "payment.captured",
            "verified": verified,
            "amount_cents": 60000,
            "currency": "USD",
            "invoice_id": invoice,
            "paid_at": "2026-10-01",
        },
    )
    return entry.id


def _shipping(invoice: str, address_match: bool = True) -> None:
    seal(
        "event",
        invoice,
        "shipment created",
        {
            "type": "shipment.created",
            "verified": True,
            "invoice_id": invoice,
            "tracking_number": "1Z999",
            "carrier": "UPS",
            "shipped_at": "2026-10-03",
            "address_match": address_match,
        },
    )
    seal(
        "event",
        invoice,
        "delivery confirmed",
        {
            "type": "delivery.confirmed",
            "verified": True,
            "invoice_id": invoice,
            "tracking_number": "1Z999",
            "delivered_at": "2026-10-05",
        },
    )


def _approval_tool() -> str:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT tool FROM approvals ORDER BY created_at DESC LIMIT 1")
            row = cur.fetchone()
    return row["tool"] if row else ""


def _llm_pack() -> EvidencePack:
    return EvidencePack(
        dispute_id="PP-D-INJECT",
        reason="UNAUTHORIZED",
        classification="friendly_fraud",
        confidence=0.99,
        checklist={
            "tracking_online": True,
            "delivered": True,
            "address_match": True,
            "shipped_in_7_days": True,
        },
        facts=[Fact(claim="Invented delivery", ledger_entry_id=999999)],
        note_to_paypal="Invented note",
        recommended_action="provide_evidence",
    )


def test_delivered_inr_recommends_evidence_with_citations() -> None:
    _payment("INV-D1")
    _shipping("INV-D1")

    out = handle(_event("PP-D-T1", "INV-D1", "MERCHANDISE_OR_SERVICE_NOT_RECEIVED"), AgentContext("defender"))

    assert out.recommended_action == "provide_evidence"
    assert out.classification == "friendly_fraud"
    assert all(out.checklist.values())
    assert out.facts
    assert all(fact.ledger_entry_id for fact in out.facts)
    assert _approval_tool() == "provide_dispute_evidence"


def test_missing_tracking_recommends_refund() -> None:
    _payment("INV-D2")

    out = handle(_event("PP-D-T2", "INV-D2", "MERCHANDISE_OR_SERVICE_NOT_RECEIVED"), AgentContext("defender"))

    assert out.recommended_action == "offer_refund"
    assert out.checklist["tracking_online"] is False
    assert _approval_tool() == "make_dispute_offer"


def test_duplicate_without_evidence_accepts_claim() -> None:
    _payment("INV-D3")

    out = handle(_event("PP-D-T3", "INV-D3", "DUPLICATE_TRANSACTION"), AgentContext("defender"))

    assert out.recommended_action == "accept_claim"
    assert _approval_tool() == "accept_dispute_claim"


def test_unverified_payment_is_not_cited() -> None:
    _payment("INV-D5", verified=False)
    _shipping("INV-D5")

    out = handle(_event("PP-D-T5", "INV-D5", "MERCHANDISE_OR_SERVICE_NOT_RECEIVED"), AgentContext("defender"))

    assert all("payment" not in fact.claim.lower() for fact in out.facts)
    assert out.recommended_action == "offer_refund"


def test_llm_cannot_add_uncited_facts(monkeypatch) -> None:
    monkeypatch.setattr(agent_base, "llm_complete", lambda system, user, schema: _llm_pack())

    out = handle(_event("PP-D-T4", "INV-D4", "UNAUTHORIZED"), AgentContext("defender"))

    assert all(fact.ledger_entry_id != 999999 for fact in out.facts)
    assert out.recommended_action != "provide_evidence"
