"""M6 gateway tests."""
from app.db import conn
from app.gateway import gateway


def test_kill_switch_denies(monkeypatch) -> None:
    from app.config import get_settings
    monkeypatch.setenv("KILL_SWITCH", "true")
    get_settings.cache_clear()
    try:
        d = gateway.call("sentinel", "get_invoice", {"invoice_id": "INV-1"}, "r")
    finally:
        monkeypatch.delenv("KILL_SWITCH")
        get_settings.cache_clear()
    assert d.outcome == "deny"


def test_console_kill_switch_denies() -> None:
    with conn() as c:
        c.execute("INSERT INTO settings (key, value) VALUES ('kill_switch', 'true')")
        c.commit()
    d = gateway.call("sentinel", "get_invoice", {"invoice_id": "INV-1"}, "r")
    assert d.outcome == "deny"


def test_unknown_tool_denies() -> None:
    d = gateway.call("sentinel", "create_refund", {"invoice_id": "INV-1"}, "r")
    assert d.outcome == "deny"


def test_sentinel_create_refund_denies() -> None:
    d = gateway.call("sentinel", "create_refund", {"invoice_id": "INV-1"}, "r")
    assert d.outcome == "deny"


def test_defender_provide_dispute_evidence_holds() -> None:
    d = gateway.call(
        "defender",
        "provide_dispute_evidence",
        {"dispute_id": "PP-D-1", "amount_cents": 60000},
        "evidence",
    )
    assert d.outcome == "hold"
    assert d.approval_id is not None
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT id, agent, tool, status FROM approvals WHERE id=%s", (d.approval_id,))
            row = cur.fetchone()
    assert row is not None
    assert row["agent"] == "defender"
    assert row["tool"] == "provide_dispute_evidence"
    assert row["status"] == "pending"


def test_collector_get_invoice_allows() -> None:
    d = gateway.call("collector", "get_invoice", {"invoice_id": "INV-1"}, "r")
    assert d.outcome == "allow"