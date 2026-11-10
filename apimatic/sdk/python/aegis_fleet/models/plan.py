from __future__ import annotations

from typing import Any

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, RFC3339DateTime, SdkBaseModel
from .enums.status3 import Status3OrStr


class Plan(SdkBaseModel):
    """Plan object"""

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

    title: str
    """Title"""

    subject_id: str
    """What this is about: an invoice, dispute or email id"""

    due_at: RFC3339DateTime
    """Due at"""

    status: Status3OrStr
    """Current status"""

    outcome: Optional[Any] = UNSET
    """allow, hold or deny"""

    created_at: RFC3339DateTime
    """When it was created (ISO 8601)"""

    updated_at: RFC3339DateTime
    """Updated at"""


class PlanDict(TypedDict):
    id: str
    agent: str
    tool: str
    args: Any
    reason: str
    title: str
    subject_id: str
    due_at: RFC3339DateTime
    status: Status3OrStr
    outcome: NotRequired[Any]
    created_at: RFC3339DateTime
    updated_at: RFC3339DateTime
