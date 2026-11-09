"""CLI runner: python -m app.agents.run <agent> <json path|dir> [--steps]."""
from __future__ import annotations

import argparse
import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.agents.base import AgentContext
from app.models import Event

SOURCE_BY_TYPE = {
    "email.received": "inbox",
    "invoice.sent": "scheduler",
    "invoice.overdue": "scheduler",
    "payment.captured": "paypal",
    "payment.refunded": "paypal",
    "dispute.created": "paypal",
    "dispute.updated": "paypal",
    "dispute.resolved": "paypal",
    "shipment.created": "courier",
    "delivery.confirmed": "courier",
}


def _files(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.glob("*.json"))
    return [path]


def _subject_id(data: dict, path: Path) -> str:
    return str(
        data.get("subject_id")
        or data.get("invoice_id")
        or data.get("dispute_id")
        or (data.get("dispute") or {}).get("dispute_id")
        or path.stem
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one AegisFleet agent over fixture JSON")
    parser.add_argument("agent")
    parser.add_argument("path")
    parser.add_argument("--steps", action="store_true", help="print agent steps after the result")
    args = parser.parse_args()

    mod = importlib.import_module(f"app.agents.{args.agent}")
    for path in _files(Path(args.path)):
        data = json.loads(path.read_text(encoding="utf-8"))
        event_type = data.get("type", "email.received")
        event = Event(
            id=str(uuid4()),
            type=event_type,
            source=SOURCE_BY_TYPE.get(event_type, "console"),
            subject_id=_subject_id(data, path),
            data=data,
            verified=bool(data.get("verified", False)),
            received_at=datetime.now(timezone.utc),
        )
        ctx = AgentContext(args.agent)
        result = mod.handle(event, ctx)
        print(result.model_dump_json(indent=2))
        if args.steps:
            print(json.dumps(ctx.steps, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
