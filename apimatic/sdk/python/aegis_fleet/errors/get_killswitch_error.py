from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError

GetKillswitchErrorBody: TypeAlias = RawError


@dataclass(frozen=True, slots=True)
class _GetKillswitchError:
    def map(self, status_code: int, content: bytes) -> GetKillswitchErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case _:
                return RawError(status_code, content)


get_killswitch_error_mapper: Final[ErrorMapper[GetKillswitchErrorBody]] = _GetKillswitchError()
