from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel
from .validation_error import ValidationError, ValidationErrorDict


class HttpValidationError(SdkBaseModel):
    """HTTPValidationError object"""

    detail: Optional[list[ValidationError]] = UNSET
    """Validation errors"""


class HttpValidationErrorDict(TypedDict):
    detail: NotRequired[list[ValidationErrorDict]]
