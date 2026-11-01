"""LLM wrapper (M7). Only fake provider implemented here."""
import json
from pathlib import Path

from pydantic import BaseModel, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES = REPO_ROOT / "fixtures" / "llm"


class LLMError(Exception):
    pass


def complete(system: str, user: str, schema: type[BaseModel]) -> BaseModel:
    from app.config import get_settings
    provider = get_settings().llm_provider
    if provider == "fake":
        return _fake(system, user, schema)
    raise NotImplementedError("set at M0")


def _fake(system: str, user: str, schema: type[BaseModel]) -> BaseModel:
    path = FIXTURES / f"{schema.__name__}.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise LLMError(f"no fixture for schema {schema.__name__}")
    except json.JSONDecodeError as e:
        raise LLMError(f"bad fixture JSON for {schema.__name__}: {e}")
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        # One retry with the validation error appended.
        try:
            return schema.model_validate({**data, "_retry_hint": str(e)})
        except ValidationError:
            raise LLMError(f"schema validation failed for {schema.__name__}: {e}")