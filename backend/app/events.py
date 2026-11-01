"""Event store + router (M5)."""
import importlib
import json
import uuid
from datetime import datetime, timezone

from app.config import ROUTES, get_settings
from app.db import conn
from app.ledger import seal
from app.models import Event


def store_event(event: Event) -> None:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "INSERT INTO events (id, paypal_event_id, type, source, subject_id, data, verified, rejected) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING",
                (
                    event.id, event.data.get("id") if event.source == "paypal" else None, event.type, event.source, event.subject_id,
                    json.dumps(event.data), event.verified, False,
                ),
            )
        c.commit()


def route(event: Event) -> None:
    """Seal the event, then run the routed agent (best-effort, never crash)."""
    seal(
        kind="event",
        subject_id=event.subject_id,
        summary=f"{event.type} from {event.source}",
        payload={"event_id": event.id, "type": event.type, "source": event.source, "verified": event.verified},
    )
    settings = get_settings()
    agent = ROUTES.get(event.type)
    if not agent or agent not in settings.agents_enabled:
        return
    run_id = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc)
    output = None
    status = "done"
    steps: list[dict] = []
    try:
        mod = importlib.import_module(f"app.agents.{agent}")
        from app.agents.base import AgentContext
        ctx = AgentContext(agent, run_id)
        result = mod.handle(event, ctx)
        output = result.model_dump()
        steps = ctx.steps
    except Exception as e:  # noqa: BLE001 — agent failures must never crash the router
        status = "failed"
        steps.append({"kind": "note", "summary": f"agent error: {e}"})
    finished_at = datetime.now(timezone.utc)
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "INSERT INTO agent_runs (id, agent, event_id, event_type, status, steps, output, started_at, finished_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    run_id, agent, event.id, event.type, status,
                    json.dumps(steps), json.dumps(output) if output else None,
                    started_at, finished_at,
                ),
            )
        c.commit()