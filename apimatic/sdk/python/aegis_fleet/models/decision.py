from __future__ import annotations

from typing import Any

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel
from .enums.outcome import OutcomeOrStr


class Decision(SdkBaseModel):
    """Decision object"""

    outcome: OutcomeOrStr
    """allow, hold or deny"""

    reason: str
    """Why"""

    approval_id: Optional[str] = UNSET
    """Id of the pending approval for this action"""

    result: Optional[Any] = UNSET
    """What the executed tool returned"""

    ledger_entry_id: int
    """Ledger entry that seals this"""


class DecisionDict(TypedDict):
    outcome: OutcomeOrStr
    reason: str
    approval_id: NotRequired[str]
    result: NotRequired[Any]
    ledger_entry_id: int
