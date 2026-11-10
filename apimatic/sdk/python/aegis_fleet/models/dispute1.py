from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, RFC3339DateTime, SdkBaseModel


class Dispute1(SdkBaseModel):
    """The dispute"""

    id: str
    """Unique id"""

    invoice_id: Optional[str] = UNSET
    """Invoice id, e.g. INV-0007"""

    reason: str
    """Why"""

    status: str
    """Current status"""

    amount_cents: Optional[int] = UNSET
    """Amount in minor units (cents)"""

    currency: Optional[str] = UNSET
    """ISO 4217 currency code"""

    buyer_name: Optional[str] = UNSET
    """Buyer's name as PayPal reports it"""

    created_at: RFC3339DateTime
    """When it was created (ISO 8601)"""

    due_by: Optional[str] = UNSET
    """Seller response deadline (ISO 8601)"""


class Dispute1Dict(TypedDict):
    id: str
    invoice_id: NotRequired[str]
    reason: str
    status: str
    amount_cents: NotRequired[int]
    currency: NotRequired[str]
    buyer_name: NotRequired[str]
    created_at: RFC3339DateTime
    due_by: NotRequired[str]
