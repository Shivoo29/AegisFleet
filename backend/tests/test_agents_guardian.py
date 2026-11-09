"""Guardian guard tests with the fake PayPal and fake LLM providers."""
from datetime import datetime, timezone
from uuid import uuid4

import app.agents.base as agent_base
from app.agents.base import AgentContext
from app.agents.guardian import handle
from app.ledger import find, seal
from app.models import Event, HealthReport


def _event(type_: str, data: dict, subject_id: str) -> Event:
    return Event(
        id=str(uuid4()),
        type=type_,
        source="courier" if type_ == "delivery.confirmed" else "console",
        subject_id=subject_id,
        data=data,
        verified=True,
        received_at=datetime.now(timezone.utc),
    )


def _payment(invoice: str) -> None:
    seal(
        "event",
        invoice,
        "payment captured",
        {
            "type": "payment.captured",
            "verified": True,
            "invoice_id": invoice,
            "amount_cents": 60000,
            "currency": "USD",
            "paid_at": datetime.now(timezone.utc).isoformat(),
        },
    )


def _shipment(invoice: str, tracking: str = "1Z-GUARD") -> None:
    seal(
        "event",
        invoice,
        "shipment created",
        {
            "type": "shipment.created",
            "verified": True,
            "invoice_id": invoice,
            "tracking_number": tracking,
            "carrier": "UPS",
            "shipped_at": datetime.now(timezone.utc).isoformat(),
        },
    )


def _dispute(dispute_id: str, invoice: str) -> None:
    seal(
        "event",
        dispute_id,
        "dispute created",
        {
            "type": "dispute.created",
            "verified": True,
            "invoice_id": invoice,
            "amount_cents": 60000,
            "currency": "USD",
        },
    )


def _guardian_decisions(subject_id: str) -> list:
    return [
        entry for entry in find(kind="decision", subject_id=subject_id)
        if (entry.payload or {}).get("agent") == "guardian"
    ]


def test_shipment_created_registers_tracking() -> None:
    _payment("INV-G1")
    _shipment("INV-G1")

    report = handle(
        _event("shipment.created", {
            "invoice_id": "INV-G1", "tracking_number": "1Z-GUARD", "carrier": "UPS",
        }, "INV-G1"),
        AgentContext("guardian"),
    )

    [decision] = _guardian_decisions("INV-G1")
    assert decision.payload["tool"] == "create_shipment_tracking"
    assert decision.payload["outcome"] == "allow"
    assert decision.payload["args"]["transaction_id"] == "INV-G1"
    assert report.score == 100
    assert {factor.name for factor in report.factors} == {
        "open_disputes", "refund_rate", "tracking_coverage", "sales_spike",
    }


def test_delivery_confirmed_updates_tracking_from_shipment_ledger() -> None:
    _payment("INV-G2")
    _shipment("INV-G2", tracking="1Z-DELIVERED")

    handle(
        _event("delivery.confirmed", {"invoice_id": "INV-G2", "status": "DELIVERED"}, "INV-G2"),
        AgentContext("guardian"),
    )

    [decision] = _guardian_decisions("INV-G2")
    assert decision.payload["tool"] == "update_shipment_tracking"
    assert decision.payload["args"]["tracking_number"] == "1Z-DELIVERED"
    assert decision.payload["args"]["status"] == "DELIVERED"


def test_health_penalizes_open_dispute_and_missing_tracking() -> None:
    _payment("INV-G3")
    _shipment("INV-G3")
    _payment("INV-G4")
    _dispute("PP-D-G3", "INV-G4")

    report = handle(
        _event("payment.captured", {"invoice_id": "INV-G4", "amount_cents": 60000}, "INV-G4"),
        AgentContext("guardian"),
    )

    factors = {factor.name: factor for factor in report.factors}
    assert factors["open_disputes"].value == 1
    assert factors["tracking_coverage"].value == 50.0
    assert report.score == 70


def test_appeal_pack_is_optional_and_ledger_cited() -> None:
    _payment("INV-G5")
    _shipment("INV-G5")
    _dispute("PP-D-G5", "INV-G5")

    plain = handle(
        _event("delivery.confirmed", {"invoice_id": "INV-G5"}, "INV-G5"),
        AgentContext("guardian"),
    )
    requested = handle(
        _event("delivery.confirmed", {
            "invoice_id": "INV-G5", "request_appeal_pack": True,
        }, "INV-G5"),
        AgentContext("guardian"),
    )

    assert plain.appeal_pack is None
    assert requested.appeal_pack is not None
    assert "PP-D-G5" in requested.appeal_pack
    assert "ledger #" in requested.appeal_pack


def test_llm_cannot_override_deterministic_score(monkeypatch) -> None:
    monkeypatch.setattr(
        agent_base,
        "llm_complete",
        lambda system, user, schema: HealthReport(
            score=0,
            factors=[],
            recommendations=["LLM advice"],
            appeal_pack=None,
        ),
    )
    _payment("INV-G6")
    _shipment("INV-G6")

    report = handle(
        _event("payment.captured", {"invoice_id": "INV-G6"}, "INV-G6"),
        AgentContext("guardian"),
    )

    assert report.score == 100
    assert report.recommendations == ["LLM advice"]
