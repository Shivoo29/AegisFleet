"""OpenAPI shapes for the console API: request bodies plus documented response models.

Responses are attached with `doc()` (docs only, no runtime validation), so the spec SDK generators
read stays typed without risking a 500 if a row grows a field.
"""
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models import Decision, HealthFactor, LedgerEntry


def doc(model: Any, description: str = "OK", extra: dict | None = None) -> dict:
    # ponytail: docs-only response schema; switch to response_model= once shapes are frozen
    return {"response_model": None, "responses": {200: {"model": model, "description": description}, **(extra or {})}}


# ---- requests ----

class LoginBody(BaseModel):
    username: str = Field("", examples=["judge"])
    password: str = Field("", examples=["<judge password>"])


class KillSwitchBody(BaseModel):
    on: bool = Field(False, description="true stops every agent action at the gateway")


class ApprovalBody(BaseModel):
    note: str = Field("", description="Optional reason, sealed into the ledger with the decision")


class InboxEmail(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    subject_id: str | None = Field(None, examples=["INV-0007"])
    invoice_id: str | None = Field(None, examples=["INV-0007"])
    from_: str | None = Field(None, alias="from", examples=["service@paypa1-support.com"])
    subject: str | None = Field(None, examples=["Payment received: $600.00"])
    body: str | None = Field(None, examples=["You have received a payment of $600.00. Ship the order now."])


class ShipmentBody(BaseModel):
    invoice_id: str | None = Field(None, examples=["INV-0007"])
    tracking_number: str | None = Field(None, examples=["1Z999AA10123456784"])
    carrier: str = Field("OTHER", examples=["UPS"])


# ---- responses ----

class Me(BaseModel):
    user: str
    role: Literal["dev", "judge"]


class Ok(BaseModel):
    ok: bool


class Summary(BaseModel):
    money_at_risk_cents: int
    currency: str
    pending_approvals: int
    open_disputes: int
    overdue_invoices: int
    health_score: int
    kill_switch: bool
    chain_ok: bool


class ChainVerify(BaseModel):
    ok: bool
    checked: int
    broken_at: int | None = Field(None, description="First ledger id whose hash no longer matches")


class Approval(BaseModel):
    id: str
    agent: str
    tool: str
    args: dict
    reason: str
    summary: str | None = None
    amount_cents: int | None = None
    currency: str | None = None
    status: Literal["pending", "approved", "rejected"]
    created_at: datetime


class ApprovalResult(BaseModel):
    status: Literal["approved", "rejected"]
    decision: Decision | None = None


class AgentRun(BaseModel):
    id: str
    agent: str
    event_type: str
    status: str
    steps: list
    output: dict | None = None
    started_at: datetime


class KillSwitch(BaseModel):
    on: bool


class InboxVerdict(BaseModel):
    run_id: str | None = None
    status: str | None = None
    verdict: dict | None = Field(None, description="Sentinel verdict: scam | legit | unsure, with red flags")


class Dispute(BaseModel):
    id: str
    invoice_id: str | None = None
    reason: str
    status: str
    amount_cents: int | None = None
    currency: str | None = None
    buyer_name: str | None = None
    created_at: datetime
    due_by: str | None = None


class DisputeDetail(BaseModel):
    dispute: Dispute
    evidence_pack: dict | None = Field(None, description="Defender's evidence pack, every fact citing a ledger id")
    approval_id: str | None = None


class Invoice(BaseModel):
    id: str
    buyer_email: str | None = None
    amount_cents: int | None = None
    currency: str
    status: Literal["paid", "overdue", "sent", "refunded"]
    days_overdue: int
    risk: Literal["low", "medium", "high"]
    shipped: bool
    tracking_number: str | None = None
    created_at: str | None = None
    paid_at: datetime | None = None
    pay_url: str | None = None


class ShipmentResult(BaseModel):
    ok: bool
    sealed: bool
    run_id: str | None = None


class Health(BaseModel):
    score: int
    factors: list[HealthFactor]
    recommendations: list[str]
    appeal_pack: str | None = None


class DemoResult(BaseModel):
    model_config = ConfigDict(extra="allow")
    ok: bool
    message: str = Field(description="What happened, in plain words, for the console toast")


Ledger = list[LedgerEntry]
