from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel


class DemoResult(SdkBaseModel):
    """DemoResult object"""

    ok: bool
    """True on success"""

    message: str
    """What happened, in plain words, for the console toast"""


class DemoResultDict(TypedDict):
    ok: bool
    message: str
