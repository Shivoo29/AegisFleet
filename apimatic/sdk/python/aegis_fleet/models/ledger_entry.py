from __future__ import annotations

from typing import Any

from typing_extensions import TypedDict

from ..core import RFC3339DateTime, SdkBaseModel
from .enums.kind import KindOrStr


class LedgerEntry(SdkBaseModel):
    """LedgerEntry object"""

    id: int
    """Unique id"""

    kind: KindOrStr
    """Entry kind: event, decision, agent_step, approval or note"""

    subject_id: str
    """What this is about: an invoice, dispute or email id"""

    summary: str
    """One-line summary"""

    payload: Any
    """Sealed data for this entry"""

    prev_hash: str
    """Hash of the previous entry; empty for the first"""

    hash: str
    """SHA-256 of this entry plus the previous hash"""

    created_at: RFC3339DateTime
    """When it was created (ISO 8601)"""


class LedgerEntryDict(TypedDict):
    id: int
    kind: KindOrStr
    subject_id: str
    summary: str
    payload: Any
    prev_hash: str
    hash: str
    created_at: RFC3339DateTime
