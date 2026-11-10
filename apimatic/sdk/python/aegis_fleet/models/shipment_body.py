from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel


class ShipmentBody(SdkBaseModel):
    """ShipmentBody object"""

    invoice_id: Optional[str] = UNSET
    """Invoice id, e.g. INV-0007"""

    tracking_number: Optional[str] = UNSET
    """Carrier tracking number"""

    carrier: str = "OTHER"
    """Shipping carrier, e.g. UPS"""


class ShipmentBodyDict(TypedDict):
    invoice_id: NotRequired[str]
    tracking_number: NotRequired[str]
    carrier: NotRequired[str]
