from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel


class Summary(SdkBaseModel):
    """Summary object"""

    money_at_risk_cents: int
    """Total held for approval, in cents"""

    currency: str
    """ISO 4217 currency code"""

    pending_approvals: int
    """Actions waiting for a human"""

    open_disputes: int
    """Number of open disputes"""

    overdue_invoices: int
    """Number of overdue invoice events"""

    health_score: int
    """Account health score, 0-100"""

    kill_switch: bool
    """True when the kill switch blocks all agent actions"""

    chain_ok: bool
    """True when every ledger hash still matches"""


class SummaryDict(TypedDict):
    money_at_risk_cents: int
    currency: str
    pending_approvals: int
    open_disputes: int
    overdue_invoices: int
    health_score: int
    kill_switch: bool
    chain_ok: bool
