from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import SdkBaseModel


class ApprovalBody(SdkBaseModel):
    """ApprovalBody object"""

    note: str = ""
    """Optional reason, sealed into the ledger with the decision"""


class ApprovalBodyDict(TypedDict):
    note: NotRequired[str]
