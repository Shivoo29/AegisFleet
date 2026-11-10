from __future__ import annotations

from typing import Any

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel


class InboxVerdict(SdkBaseModel):
    """InboxVerdict object"""

    run_id: Optional[str] = UNSET
    """Agent run id"""

    status: Optional[str] = UNSET
    """Current status"""

    verdict: Optional[Any] = UNSET
    """Sentinel verdict: scam | legit | unsure, with red flags"""


class InboxVerdictDict(TypedDict):
    run_id: NotRequired[str]
    status: NotRequired[str]
    verdict: NotRequired[Any]
