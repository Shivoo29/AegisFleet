from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError, decode_json
from ..models.http_validation_error import HttpValidationError

InboxErrorBody: TypeAlias = HttpValidationError | RawError


@dataclass(frozen=True, slots=True)
class _InboxError:
    def map(self, status_code: int, content: bytes) -> InboxErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case 422:
                return decode_json[HttpValidationError](content)
            case _:
                return RawError(status_code, content)


inbox_error_mapper: Final[ErrorMapper[InboxErrorBody]] = _InboxError()
