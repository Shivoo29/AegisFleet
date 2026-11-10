from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError

LedgerVerifyErrorBody: TypeAlias = RawError


@dataclass(frozen=True, slots=True)
class _LedgerVerifyError:
    def map(self, status_code: int, content: bytes) -> LedgerVerifyErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case _:
                return RawError(status_code, content)


ledger_verify_error_mapper: Final[ErrorMapper[LedgerVerifyErrorBody]] = _LedgerVerifyError()
