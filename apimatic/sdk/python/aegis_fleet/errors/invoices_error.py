from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError

InvoicesErrorBody: TypeAlias = RawError


@dataclass(frozen=True, slots=True)
class _InvoicesError:
    def map(self, status_code: int, content: bytes) -> InvoicesErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case _:
                return RawError(status_code, content)


invoices_error_mapper: Final[ErrorMapper[InvoicesErrorBody]] = _InvoicesError()
