"""Write the backend's OpenAPI spec to docs/api/openapi.json (input for APIMatic SDKs and docs portal).

Run from backend/: python ../scripts/export_openapi.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.main import app  # noqa: E402

out = Path(__file__).resolve().parents[1] / "docs" / "api" / "openapi.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(app.openapi(), indent=2) + "\n", encoding="utf-8")
print(f"wrote {out}")
