from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError

LogoutErrorBody: TypeAlias = RawError


@dataclass(frozen=True, slots=True)
class _LogoutError:
    def map(self, status_code: int, content: bytes) -> LogoutErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case _:
                return RawError(status_code, content)


logout_error_mapper: Final[ErrorMapper[LogoutErrorBody]] = _LogoutError()
