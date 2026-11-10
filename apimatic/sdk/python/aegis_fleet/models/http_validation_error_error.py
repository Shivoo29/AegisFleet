from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel
from .validation_error import ValidationError, ValidationErrorDict


class HttpValidationErrorError(SdkBaseModel):
    """HTTPValidationError object"""

    detail: Optional[list[ValidationError]] = UNSET
    """Validation errors"""


class HttpValidationErrorErrorDict(TypedDict):
    detail: NotRequired[list[ValidationErrorDict]]
