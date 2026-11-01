"""CLI runner: python -m app.agents.run <agent> <json path>"""
import json
import sys
from datetime import datetime, timezone
from uuid import uuid4

from app.agents.base import AgentContext
from app.models import Event


def main() -> None:
    if len(sys.argv) < 3:
        print("usage: python -m app.agents.run <agent> <json path>")
        sys.exit(2)
    agent = sys.argv[1]
    path = sys.argv[2]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    import importlib
    mod = importlib.import_module(f"app.agents.{agent}")
    ev = Event(
        id=str(uuid4()),
        type=data.get("type", "email.received"),
        source="console",
        subject_id=data.get("subject_id", "test"),
        data=data,
        verified=False,
        received_at=datetime.now(timezone.utc),
    )
    ctx = AgentContext(agent)
    result = mod.handle(ev, ctx)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()