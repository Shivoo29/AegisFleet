from __future__ import annotations

from pydantic import Field
from typing_extensions import TypedDict

from ..core import SdkBaseModel
from .unions.loc import Loc, LocDict


class ValidationError(SdkBaseModel):
    """ValidationError object"""

    loc: list[Loc]
    """Where the invalid value is"""

    msg: str
    """Error message"""

    type_: str = Field(alias="type")
    """Error type"""


class ValidationErrorDict(TypedDict):
    loc: list[LocDict]
    msg: str
    type_: str
