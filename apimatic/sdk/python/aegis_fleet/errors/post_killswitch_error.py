from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError, decode_json
from ..models.http_validation_error import HttpValidationError

PostKillswitchErrorBody: TypeAlias = HttpValidationError | RawError


@dataclass(frozen=True, slots=True)
class _PostKillswitchError:
    def map(self, status_code: int, content: bytes) -> PostKillswitchErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case 422:
                return decode_json[HttpValidationError](content)
            case _:
                return RawError(status_code, content)


post_killswitch_error_mapper: Final[ErrorMapper[PostKillswitchErrorBody]] = _PostKillswitchError()
