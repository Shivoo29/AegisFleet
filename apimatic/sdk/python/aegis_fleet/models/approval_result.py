from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel
from .decision2 import Decision2, Decision2Dict
from .enums.status1 import Status1OrStr


class ApprovalResult(SdkBaseModel):
    """ApprovalResult object"""

    status: Status1OrStr
    """Current status"""

    decision: Optional[Decision2] = UNSET
    """Gateway decision for the executed action"""


class ApprovalResultDict(TypedDict):
    status: Status1OrStr
    decision: NotRequired[Decision2Dict]
