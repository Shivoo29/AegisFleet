from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError

HealthErrorBody: TypeAlias = RawError


@dataclass(frozen=True, slots=True)
class _HealthError:
    def map(self, status_code: int, content: bytes) -> HealthErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case _:
                return RawError(status_code, content)


health_error_mapper: Final[ErrorMapper[HealthErrorBody]] = _HealthError()
