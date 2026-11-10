from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError

McpLinkErrorBody: TypeAlias = RawError


@dataclass(frozen=True, slots=True)
class _McpLinkError:
    def map(self, status_code: int, content: bytes) -> McpLinkErrorBody:
        match status_code:
            case 401:
                return RawError(status_code, content)
            case _:
                return RawError(status_code, content)


mcp_link_error_mapper: Final[ErrorMapper[McpLinkErrorBody]] = _McpLinkError()
