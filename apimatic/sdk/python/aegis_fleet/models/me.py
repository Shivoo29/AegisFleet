from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel
from .enums.role import RoleOrStr


class Me(SdkBaseModel):
    """Me object"""

    user: str
    """Logged-in user name"""

    role: RoleOrStr
    """dev (seller) or judge"""


class MeDict(TypedDict):
    user: str
    role: RoleOrStr
