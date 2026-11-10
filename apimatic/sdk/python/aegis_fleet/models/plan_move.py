from __future__ import annotations

from typing_extensions import TypedDict

from ..core import RFC3339DateTime, SdkBaseModel


class PlanMove(SdkBaseModel):
    """PlanMove object"""

    due_at: RFC3339DateTime
    """New time to run it (ISO 8601)"""


class PlanMoveDict(TypedDict):
    due_at: RFC3339DateTime
