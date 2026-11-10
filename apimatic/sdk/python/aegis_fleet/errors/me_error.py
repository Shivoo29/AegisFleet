from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError

MeErrorBody: TypeAlias = RawError


@dataclass(frozen=True, slots=True)
class _MeError:
    def map(self, status_code: int, content: bytes) -> MeErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case _:
                return RawError(status_code, content)


me_error_mapper: Final[ErrorMapper[MeErrorBody]] = _MeError()
