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

def test_reminder_cap_denies_third_call() -> None:
    args = {"invoice_id": "INV-7"}
    outs = [gateway.call("collector", "send_invoice_reminder", args, "r").outcome for _ in range(3)]
    assert outs == ["allow", "allow", "deny"]


def test_bad_amount_denies() -> None:
    d = gateway.call("defender", "make_dispute_offer", {"dispute_id": "D", "amount_cents": -5}, "r")
    assert d.outcome == "deny"
    d = gateway.call("defender", "make_dispute_offer",
                     {"dispute_id": "D", "amount_cents": 900, "disputed_amount_cents": 500}, "r")
    assert d.outcome == "deny"


def test_first_dispute_message_holds_then_allows() -> None:
    d = gateway.call("defender", "send_dispute_message", {"dispute_id": "D-2"}, "r")
    assert d.outcome == "hold"
    assert gateway.approve(d.approval_id, "skj").outcome == "allow"
    assert gateway.call("defender", "send_dispute_message", {"dispute_id": "D-2"}, "r").outcome == "allow"


def test_approve_twice_and_reject() -> None:
    import pytest
    d = gateway.call("defender", "accept_dispute_claim", {"dispute_id": "D-3"}, "r")
    gateway.reject(d.approval_id, "skj", "no")
    with pytest.raises(KeyError):
        gateway.approve(d.approval_id, "skj")


def test_approve_api() -> None:
    from fastapi.testclient import TestClient
    from app.main import app
    d = gateway.call("defender", "provide_dispute_evidence", {"dispute_id": "D-4"}, "r")
    cl = TestClient(app)
    r = cl.post(f"/api/approvals/{d.approval_id}/approve", json={"note": "ok"}, auth=("skj", "dev"))
    assert r.status_code == 200 and r.json()["decision"]["outcome"] == "allow"
    assert cl.post(f"/api/approvals/{d.approval_id}/approve", auth=("skj", "dev")).status_code == 409
    from app.ledger import verify
    assert verify()["ok"]


def test_demo_records_never_reach_paypal_in_sandbox(monkeypatch) -> None:
    """Seeded ids run on the fake client and are sealed as simulated, even with PAYPAL_MODE=sandbox."""
    from app.config import get_settings
    from app.paypal import client as pp
    monkeypatch.setenv("PAYPAL_MODE", "sandbox")
    monkeypatch.setenv("CONSOLE_PASSWORD", "not-dev")
    get_settings.cache_clear()
    monkeypatch.setattr(pp.PayPalClient, "_req", lambda *a, **k: (_ for _ in ()).throw(AssertionError("hit PayPal")))
    try:
        d = gateway.call("collector", "get_invoice", {"invoice_id": "INV-0007"}, "r")
    finally:
        get_settings.cache_clear()
    assert d.outcome == "allow" and d.result["simulated"] is True
