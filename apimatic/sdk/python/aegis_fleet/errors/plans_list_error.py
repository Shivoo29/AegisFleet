from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError

PlansListErrorBody: TypeAlias = RawError


@dataclass(frozen=True, slots=True)
class _PlansListError:
    def map(self, status_code: int, content: bytes) -> PlansListErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case _:
                return RawError(status_code, content)


plans_list_error_mapper: Final[ErrorMapper[PlansListErrorBody]] = _PlansListError()
