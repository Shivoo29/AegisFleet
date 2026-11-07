"""M5 webhook tests: dedupe, money facts sealed, unverified not routed."""
from fastapi.testclient import TestClient

from app.db import conn
from app.ledger import find
from app.main import app

CAPTURE = {"id": "WH-1", "event_type": "PAYMENT.CAPTURE.COMPLETED",
           "resource": {"id": "CAP-9", "invoice_id": "INV-0007",
                        "amount": {"value": "600.00", "currency_code": "USD"}}}


def _events() -> list:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT id, rejected FROM events")
            return cur.fetchall()


def test_capture_sealed_with_money_and_deduped() -> None:
    cl = TestClient(app)
    assert cl.post("/webhooks/paypal", json=CAPTURE).json() == {"ok": True}
    assert cl.post("/webhooks/paypal", json=CAPTURE).json()["duplicate"] is True
    assert len(_events()) == 1
    [e] = find(kind="event", subject_id="INV-0007")
    assert e.payload["amount_cents"] == 60000
    assert e.payload["currency"] == "USD"
    assert e.payload["verified"] is True


def test_unknown_type_ignored() -> None:
    r = TestClient(app).post("/webhooks/paypal", json={"id": "WH-2", "event_type": "BILLING.PLAN.CREATED"})
    assert r.json()["ignored"] is True
    assert _events() == []


def test_unverified_stored_rejected_not_routed(monkeypatch) -> None:
    from app.paypal import webhooks
    monkeypatch.setattr(webhooks, "_verified", lambda req, body: False)
    TestClient(app).post("/webhooks/paypal", json={**CAPTURE, "id": "WH-3"})
    assert [r["rejected"] for r in _events()] == [True]
    assert find(kind="event", subject_id="INV-0007") == []


def test_dispute_normalized() -> None:
    from app.paypal.webhooks import normalize
    d = normalize({"id": "WH-4", "event_type": "CUSTOMER.DISPUTE.CREATED",
                   "resource": {"dispute_id": "PP-D-12345", "dispute_amount": {"value": "12.5", "currency_code": "USD"},
                                "disputed_transactions": [{"invoice_number": "INV-0007"}]}})
    assert (d["subject_id"], d["amount_cents"], d["invoice_id"]) == ("PP-D-12345", 1250, "INV-0007")
