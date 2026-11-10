from __future__ import annotations

from pydantic import Field
from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel


class InboxEmail(SdkBaseModel):
    """InboxEmail object"""

    subject_id: Optional[str] = UNSET
    """What this is about: an invoice, dispute or email id"""

    invoice_id: Optional[str] = UNSET
    """Invoice id, e.g. INV-0007"""

    from_: Optional[str] = Field(default=UNSET, alias="from")
    """Sender address"""

    subject: Optional[str] = UNSET
    """Email subject"""

    body: Optional[str] = UNSET
    """Email body text"""


class InboxEmailDict(TypedDict):
    subject_id: NotRequired[str]
    invoice_id: NotRequired[str]
    from_: NotRequired[str]
    subject: NotRequired[str]
    body: NotRequired[str]
