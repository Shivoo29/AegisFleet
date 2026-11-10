from __future__ import annotations

from typing import Any

from typing_extensions import TypedDict

from ..core import SdkBaseModel


class HealthFactor(SdkBaseModel):
    """HealthFactor object"""

    name: str
    """Factor name"""

    value: Any
    """Measured value"""

    impact: str
    """How this factor moves the score"""

    note: str
    """Free-text note"""


class HealthFactorDict(TypedDict):
    name: str
    value: Any
    impact: str
    note: str
