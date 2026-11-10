from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel


class Ok(SdkBaseModel):
    """Ok object"""

    ok: bool
    """True on success"""


class OkDict(TypedDict):
    ok: bool
