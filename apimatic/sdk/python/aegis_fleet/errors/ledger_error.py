from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError, decode_json
from ..models.http_validation_error import HttpValidationError

LedgerErrorBody: TypeAlias = HttpValidationError | RawError


@dataclass(frozen=True, slots=True)
class _LedgerError:
    def map(self, status_code: int, content: bytes) -> LedgerErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case 422:
                return decode_json[HttpValidationError](content)
            case _:
                return RawError(status_code, content)


ledger_error_mapper: Final[ErrorMapper[LedgerErrorBody]] = _LedgerError()
