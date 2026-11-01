"""All shared Pydantic contracts (M2). Frozen — change only via PR approved by SKJ."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

EventType = Literal[
    "invoice.sent",
    "invoice.overdue",
    "invoice.paid",
    "payment.captured",
    "payment.refunded",
    "email.received",
    "shipment.created",
    "delivery.confirmed",
    "dispute.created",
    "dispute.updated",
    "dispute.resolved",
]


class Event(BaseModel):
    id: str
    type: EventType
    source: Literal["paypal", "inbox", "courier", "scheduler", "console"]
    subject_id: str
    data: dict
    verified: bool
    received_at: datetime


class Decision(BaseModel):
    outcome: Literal["allow", "hold", "deny"]
    reason: str
    approval_id: str | None = None
    result: dict | None = None
    ledger_entry_id: int


class LedgerEntry(BaseModel):
    id: int
    kind: Literal["event", "decision", "agent_step", "approval", "note"]
    subject_id: str
    summary: str
    payload: dict
    prev_hash: str
    hash: str
    created_at: datetime


# --- Agent outputs (exactly as Notion "Architecture & contracts" §7) ---


class SentinelVerdict(BaseModel):
    verdict: Literal["scam", "legit", "unsure"]
    confidence: float
    matched_payment_entry_id: int | None = None
    red_flags: list[str] = []
    explanation: str = ""


class Fact(BaseModel):
    claim: str
    ledger_entry_id: int


class EvidencePack(BaseModel):
    dispute_id: str
    reason: str
    classification: Literal["friendly_fraud", "genuine", "unclear"]
    confidence: float
    checklist: dict[str, bool]
    facts: list[Fact]
    note_to_paypal: str
    recommended_action: Literal["provide_evidence", "offer_refund", "accept_claim"]


class CollectorPlan(BaseModel):
    invoice_id: str
    risk: Literal["low", "med", "high"]
    days_overdue: int
    tone: Literal["friendly", "firm", "final"]
    reminder_note: str
    next_action: Literal["remind", "wait", "escalate"]


class HealthFactor(BaseModel):
    name: str
    value: object
    impact: str
    note: str


class HealthReport(BaseModel):
    score: int
    factors: list[HealthFactor]
    recommendations: list[str]
    appeal_pack: str | None = None