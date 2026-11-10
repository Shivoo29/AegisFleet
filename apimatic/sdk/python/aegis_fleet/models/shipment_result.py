from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel


class ShipmentResult(SdkBaseModel):
    """ShipmentResult object"""

    ok: bool
    """True on success"""

    sealed: bool
    """True once the event is in the ledger"""

    run_id: Optional[str] = UNSET
    """Agent run id"""


class ShipmentResultDict(TypedDict):
    ok: bool
    sealed: bool
    run_id: NotRequired[str]
