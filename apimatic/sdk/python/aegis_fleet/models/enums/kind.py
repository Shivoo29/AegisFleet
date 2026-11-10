from enum import Enum
from typing import Annotated, TypeAlias

from ...core import open_enum_validator


class Kind(str, Enum):
    """Entry kind: event, decision, agent_step, approval or note"""

    EVENT = "event"
    DECISION = "decision"
    AGENT_STEP = "agent_step"
    APPROVAL = "approval"
    NOTE = "note"

    __str__ = str.__str__


KindOrStr: TypeAlias = Annotated[Kind | str, open_enum_validator(Kind)]
