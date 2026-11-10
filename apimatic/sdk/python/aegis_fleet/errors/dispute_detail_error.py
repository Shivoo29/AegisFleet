from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError, decode_json
from ..models.http_validation_error import HttpValidationError

DisputeDetailErrorBody: TypeAlias = HttpValidationError | RawError


@dataclass(frozen=True, slots=True)
class _DisputeDetailError:
    def map(self, status_code: int, content: bytes) -> DisputeDetailErrorBody:
        match status_code:
            case 401 | 404:
                return RawError(status_code, content)
            case 422:
                return decode_json[HttpValidationError](content)
            case _:
                return RawError(status_code, content)


dispute_detail_error_mapper: Final[ErrorMapper[DisputeDetailErrorBody]] = _DisputeDetailError()
