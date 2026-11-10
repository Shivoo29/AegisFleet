from __future__ import annotations

from typing import Any

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel
from .dispute1 import Dispute1, Dispute1Dict


class DisputeDetail(SdkBaseModel):
    """DisputeDetail object"""

    dispute: Dispute1
    """The dispute"""

    evidence_pack: Optional[Any] = UNSET
    """Defender's evidence pack, every fact citing a ledger id"""

    approval_id: Optional[str] = UNSET
    """Id of the pending approval for this action"""


class DisputeDetailDict(TypedDict):
    dispute: Dispute1Dict
    evidence_pack: NotRequired[Any]
    approval_id: NotRequired[str]
