from __future__ import annotations

from typing import Any

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, RFC3339DateTime, SdkBaseModel


class AgentRun(SdkBaseModel):
    """AgentRun object"""

    id: str
    """Unique id"""

    agent: str
    """Agent name: sentinel, defender, guardian or collector"""

    event_type: str
    """Event that started the run, e.g. dispute.created"""

    status: str
    """Current status"""

    steps: list[Any]
    """Each step the agent took"""

    output: Optional[Any] = UNSET
    """Agent's structured result"""

    started_at: RFC3339DateTime
    """When the run started (ISO 8601)"""


class AgentRunDict(TypedDict):
    id: str
    agent: str
    event_type: str
    status: str
    steps: list[Any]
    output: NotRequired[Any]
    started_at: RFC3339DateTime
