"""Shared pytest fixtures."""
import os

os.environ.setdefault("PAYPAL_MODE", "fake")
os.environ.setdefault("LLM_PROVIDER", "fake")
os.environ.setdefault("AGENTS_ENABLED", "collector,sentinel,guardian,defender")
os.environ.setdefault("CONSOLE_PASSWORD", "dev")
os.environ.setdefault("DEMO_MODE", "true")
os.environ.setdefault("KILL_SWITCH", "false")
os.environ.setdefault("APPROVAL_THRESHOLD_CENTS", "10000")

import pytest

from app.db import conn, init_schema


@pytest.fixture(scope="session", autouse=True)
def _init_schema() -> None:
    init_schema()


@pytest.fixture(autouse=True)
def _truncate() -> None:
    with conn() as c:
        with c.cursor() as cur:
            for t in ("approvals", "ledger", "agent_runs", "budgets", "events", "invoices", "shipments", "settings"):
                cur.execute(f"TRUNCATE {t} RESTART IDENTITY CASCADE")
        c.commit()