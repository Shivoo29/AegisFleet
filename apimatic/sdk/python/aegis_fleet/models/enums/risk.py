from enum import Enum
from typing import Annotated, TypeAlias

from ...core import open_enum_validator


class Risk(str, Enum):
    """Payment risk: low, medium or high"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    __str__ = str.__str__


RiskOrStr: TypeAlias = Annotated[Risk | str, open_enum_validator(Risk)]
