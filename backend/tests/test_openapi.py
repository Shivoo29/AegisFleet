"""The committed OpenAPI spec (APIMatic's input) must match the live app."""
import json
from pathlib import Path

from app.main import app

SPEC = Path(__file__).resolve().parents[2] / "docs" / "api" / "openapi.json"


def test_committed_spec_is_current() -> None:
    assert json.loads(SPEC.read_text(encoding="utf-8")) == json.loads(json.dumps(app.openapi())), \
        "run: python ../scripts/export_openapi.py"
