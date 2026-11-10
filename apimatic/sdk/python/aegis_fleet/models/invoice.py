from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, RFC3339DateTime, SdkBaseModel
from .enums.risk import RiskOrStr
from .enums.status2 import Status2OrStr


class Invoice(SdkBaseModel):
    """Invoice object"""

    id: str
    """Unique id"""

    buyer_email: Optional[str] = UNSET
    """Buyer's email address"""

    amount_cents: Optional[int] = UNSET
    """Amount in minor units (cents)"""

    currency: str
    """ISO 4217 currency code"""

    status: Status2OrStr
    """Current status"""

    days_overdue: int
    """Days past the due date; 0 when paid or not yet due"""

    risk: RiskOrStr
    """Payment risk: low, medium or high"""

    shipped: bool
    """True when tracking was added"""

    tracking_number: Optional[str] = UNSET
    """Carrier tracking number"""

    created_at: Optional[str] = UNSET
    """When it was created (ISO 8601)"""

    paid_at: Optional[RFC3339DateTime] = UNSET
    """When payment was verified (ISO 8601)"""

    pay_url: Optional[str] = UNSET
    """PayPal payment page for this invoice"""


class InvoiceDict(TypedDict):
    id: str
    buyer_email: NotRequired[str]
    amount_cents: NotRequired[int]
    currency: str
    status: Status2OrStr
    days_overdue: int
    risk: RiskOrStr
    shipped: bool
    tracking_number: NotRequired[str]
    created_at: NotRequired[str]
    paid_at: NotRequired[RFC3339DateTime]
    pay_url: NotRequired[str]
