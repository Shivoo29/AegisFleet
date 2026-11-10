from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import SdkBaseModel


class LoginBody(SdkBaseModel):
    """LoginBody object"""

    username: str = ""
    """dev or judge"""

    password: str = ""
    """Console password"""


class LoginBodyDict(TypedDict):
    username: NotRequired[str]
    password: NotRequired[str]
