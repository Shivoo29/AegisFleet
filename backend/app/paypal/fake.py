"""Fake PayPal client (M4). Returns JSON from fixtures/paypal/<tool>.json."""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
FIXTURES = REPO_ROOT / "fixtures" / "paypal"


class FakePayPal:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)

        def _tool(args: dict) -> dict:
            self.calls.append((name, args))
            path = FIXTURES / f"{name}.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}

        return _tool