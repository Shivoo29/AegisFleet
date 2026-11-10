from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel
from .health_factor import HealthFactor, HealthFactorDict


class Health(SdkBaseModel):
    """Health object"""

    score: int
    """Health score, 0-100"""

    factors: list[HealthFactor]
    """What the health score is made of"""

    recommendations: list[str]
    """Steps that would raise the score"""

    appeal_pack: Optional[str] = UNSET
    """Draft appeal text Guardian wrote for PayPal, if the account is limited"""


class HealthDict(TypedDict):
    score: int
    factors: list[HealthFactorDict]
    recommendations: list[str]
    appeal_pack: NotRequired[str]
