"""Sentinel guard tests with the fake LLM provider."""
from datetime import datetime, timezone
from uuid import uuid4

import app.agents.base as agent_base
from app.agents.base import AgentContext
from app.agents.sentinel import handle
from app.ledger import seal
from app.models import Event, SentinelVerdict


def _llm_says_legit(monkeypatch) -> None:
    monkeypatch.setattr(
        agent_base,
        "llm_complete",
        lambda system, user, schema: SentinelVerdict(verdict="legit", confidence=0.99),
    )


def _event(invoice: str, body: str, sender: str = "PayPal <service@paypal.com>") -> Event:
    return Event(
        id=str(uuid4()),
        type="email.received",
        source="inbox",
        subject_id=invoice,
        data={"from": sender, "subject": "Payment", "body": body},
        verified=False,
        received_at=datetime.now(timezone.utc),
    )


def test_guard_overrides_llm_legit_without_verified_payment(monkeypatch) -> None:
    _llm_says_legit(monkeypatch)
    out = handle(
        _event("INV-5555", "You have received $600.00 for INV-5555. Funds are available."),
        AgentContext("sentinel"),
    )
    assert out.verdict == "scam"
    assert out.matched_payment_entry_id is None
    assert "Hard rule" not in out.explanation
    assert out.explanation.count(". ") <= 2


def test_llm_legit_without_any_payment_becomes_unsure(monkeypatch) -> None:
    _llm_says_legit(monkeypatch)
    out = handle(
        _event("INV-7777", "A short note with no payment claim."),
        AgentContext("sentinel"),
    )
    assert out.verdict == "unsure"


def test_verified_payment_without_amount_is_not_a_mismatch(monkeypatch) -> None:
    _llm_says_legit(monkeypatch)
    entry = seal(
        "event",
        "INV-9001",
        "payment captured",
        {"type": "payment.captured", "verified": True, "invoice_id": "INV-9001"},
    )
    out = handle(
        _event("INV-9001", "You have received $250.00 for INV-9001."),
        AgentContext("sentinel"),
    )
    assert out.verdict == "legit"
    assert out.matched_payment_entry_id == entry.id


def test_verified_payment_amount_mismatch_is_scam(monkeypatch) -> None:
    _llm_says_legit(monkeypatch)
    seal(
        "event",
        "INV-9002",
        "payment captured",
        {
            "type": "payment.captured",
            "verified": True,
            "amount_cents": 9000,
            "currency": "USD",
            "invoice_id": "INV-9002",
        },
    )
    out = handle(
        _event("INV-9002", "You have received $900.00 for INV-9002."),
        AgentContext("sentinel"),
    )
    assert out.verdict == "scam"
    assert "amount does not match" in out.explanation
