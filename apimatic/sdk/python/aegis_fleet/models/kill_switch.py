from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel


class KillSwitch(SdkBaseModel):
    """KillSwitch object"""

    on: bool
    """True when the kill switch is on"""


class KillSwitchDict(TypedDict):
    on: bool
