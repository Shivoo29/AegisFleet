from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import SdkBaseModel


class KillSwitchBody(SdkBaseModel):
    """KillSwitchBody object"""

    on: bool = False
    """true stops every agent action at the gateway"""


class KillSwitchBodyDict(TypedDict):
    on: NotRequired[bool]
