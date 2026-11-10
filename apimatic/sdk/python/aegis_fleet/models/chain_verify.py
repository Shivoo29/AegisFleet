from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel


class ChainVerify(SdkBaseModel):
    """ChainVerify object"""

    ok: bool
    """True on success"""

    checked: int
    """Number of ledger entries checked"""

    broken_at: Optional[int] = UNSET
    """First ledger id whose hash no longer matches"""


class ChainVerifyDict(TypedDict):
    ok: bool
    checked: int
    broken_at: NotRequired[int]
