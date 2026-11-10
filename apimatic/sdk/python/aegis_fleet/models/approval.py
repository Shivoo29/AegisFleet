from __future__ import annotations

from typing import Any

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, RFC3339DateTime, SdkBaseModel
from .enums.status import StatusOrStr


class Approval(SdkBaseModel):
    """Approval object"""

    id: str
    """Unique id"""

    agent: str
    """Agent name: sentinel, defender, guardian or collector"""

    tool: str
    """Gateway tool the agent called"""

    args: Any
    """Tool arguments the agent asked the gateway to run"""

    reason: str
    """Why"""

    summary: Optional[str] = UNSET
    """One-line summary"""

    amount_cents: Optional[int] = UNSET
    """Amount in minor units (cents)"""

    currency: Optional[str] = UNSET
    """ISO 4217 currency code"""

    status: StatusOrStr
    """Current status"""

    created_at: RFC3339DateTime
    """When it was created (ISO 8601)"""


class ApprovalDict(TypedDict):
    id: str
    agent: str
    tool: str
    args: Any
    reason: str
    summary: NotRequired[str]
    amount_cents: NotRequired[int]
    currency: NotRequired[str]
    status: StatusOrStr
    created_at: RFC3339DateTime
