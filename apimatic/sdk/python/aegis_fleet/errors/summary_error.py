from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError

SummaryErrorBody: TypeAlias = RawError


@dataclass(frozen=True, slots=True)
class _SummaryError:
    def map(self, status_code: int, content: bytes) -> SummaryErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case _:
                return RawError(status_code, content)


summary_error_mapper: Final[ErrorMapper[SummaryErrorBody]] = _SummaryError()
