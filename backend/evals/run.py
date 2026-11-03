"""Offline eval harness: python -m evals.run [--agent sentinel] [--reset]."""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents.base import AgentContext
from app.agents.sentinel import handle as sentinel_handle
from app.db import conn
from app.ledger import find, seal
from app.models import Event

ROOT = Path(__file__).resolve().parents[2]
EMAILS = ROOT / "fixtures" / "emails"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _reset() -> None:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("TRUNCATE ledger, agent_runs RESTART IDENTITY CASCADE")
        c.commit()


def _seed(fixture: str, subject_id: str, seeds: list[dict]) -> None:
    if not seeds:
        return
    existing = find(subject_id=subject_id, limit=500)
    if any((entry.payload or {}).get("_eval_fixture") == fixture for entry in existing):
        return
    for seed in seeds:
        payload = dict(seed.get("payload") or {})
        payload["_eval_fixture"] = fixture
        seal(
            kind=seed.get("kind", "event"),
            subject_id=subject_id,
            summary=seed.get("summary", f"eval seed for {fixture}"),
            payload=payload,
        )


def _event(data: dict, subject_id: str) -> Event:
    return Event(
        id=str(uuid4()),
        type=data.get("type", "email.received"),
        source="inbox",
        subject_id=subject_id,
        data=data,
        verified=False,
        received_at=_now(),
    )


def run_sentinel() -> int:
    results = []
    for path in sorted(EMAILS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        subject_id = str(data.get("subject_id") or data.get("invoice_id") or path.stem)
        _seed(path.stem, subject_id, data.get("ledger_seed", []))
        ctx = AgentContext("sentinel")
        started = time.perf_counter()
        error = None
        try:
            verdict = sentinel_handle(_event(data, subject_id), ctx)
            predicted = verdict.verdict
        except Exception as exc:  # noqa: BLE001
            error = f"{type(exc).__name__}: {exc}"
            predicted = "error"
        latency_ms = (time.perf_counter() - started) * 1000
        invalid_llm = any("llm error" in step.get("summary", "") for step in ctx.steps)
        results.append(
            {
                "fixture": path.name,
                "expected": data["expected"],
                "predicted": predicted,
                "latency_ms": latency_ms,
                "invalid_llm": invalid_llm,
                "error": error,
            }
        )

    n = len(results)
    correct = sum(1 for r in results if r["predicted"] == r["expected"])
    false_alarms = sum(1 for r in results if r["expected"] == "legit" and r["predicted"] == "scam")
    missed = sum(1 for r in results if r["expected"] == "scam" and r["predicted"] == "legit")
    unsure = sum(1 for r in results if r["predicted"] == "unsure")
    invalid = sum(1 for r in results if r["invalid_llm"])
    avg_latency = statistics.mean(r["latency_ms"] for r in results) if results else 0.0

    print(f"{'agent':<10}{'n':>4}{'accuracy':>10}{'false_alarms':>14}{'scams_missed':>14}{'invalid_json':>14}{'avg_latency_ms':>16}")
    print(
        f"{'sentinel':<10}{n:>4}{correct / n * 100:>9.1f}%{false_alarms:>14}{missed:>14}"
        f"{invalid / n * 100:>13.1f}%{avg_latency:>16.1f}"
    )

    for result in results:
        if result["predicted"] != result["expected"]:
            print(
                f"  FAIL {result['fixture']}: expected={result['expected']} "
                f"predicted={result['predicted']}"
            )
        if result["error"]:
            print(f"  ERROR {result['fixture']}: {result['error']}")

    print(f"\nunsure: {unsure}/{n}")
    return 0 if missed == 0 and false_alarms <= 2 and invalid == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="AegisFleet offline evals")
    parser.add_argument("--agent", choices=["sentinel"], default="sentinel")
    parser.add_argument("--reset", action="store_true", help="truncate ledger and agent_runs first")
    args = parser.parse_args()

    if args.reset:
        _reset()
    if args.agent == "sentinel":
        return run_sentinel()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
