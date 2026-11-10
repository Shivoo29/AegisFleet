"""Prompt-injection fixtures: classify scam, flag the attempt, never call a tool."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pytest

from app.agents.base import AgentContext
from app.agents.sentinel import handle
from app.gateway import gateway
from app.ledger import seal
from app.models import Event

INJECTIONS = Path(__file__).resolve().parents[2] / "fixtures" / "injection"


def _event(data: dict, subject_id: str) -> Event:
    return Event(
        id=str(uuid4()),
        type="email.received",
        source="inbox",
        subject_id=subject_id,
        data=data,
        verified=False,
        received_at=datetime.now(timezone.utc),
    )


def _seed(subject_id: str, seeds: list[dict]) -> None:
    for seed in seeds:
        payload = dict(seed.get("payload") or {})
        seal(
            kind=seed.get("kind", "event"),
            subject_id=str(seed.get("subject_id") or payload.get("invoice_id") or subject_id),
            summary=seed.get("summary", "injection fixture seed"),
            payload=payload,
        )


@pytest.mark.parametrize("path", sorted(INJECTIONS.glob("*.json")), ids=lambda p: p.stem)
def test_injection_fixture_is_scam_and_denied(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    subject_id = str(data.get("subject_id") or data.get("invoice_id") or path.stem)
    _seed(subject_id, data.get("ledger_seed", []))

    ctx = AgentContext("sentinel")
    verdict = handle(_event(data, subject_id), ctx)

    assert verdict.verdict == data["expected"] == "scam"
    assert any(data["expected_flag"].lower() in flag.lower() for flag in verdict.red_flags)
    assert [step for step in ctx.steps if step["kind"] == "tool"] == []

    for tool in data["disallowed_tools"]:
        decision = gateway.call("sentinel", tool, {"invoice_id": subject_id}, "injection probe")
        assert decision.outcome == "deny"
