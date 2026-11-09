"""M8 demo endpoints: auth, injection denied, tamper detected, reset."""
from fastapi.testclient import TestClient

from app.ledger import find
from app.main import app

AUTH = ("skj", "dev")


def test_demo_needs_password() -> None:
    assert TestClient(app).get("/api/demo/status").status_code == 401


def test_injection_denied_and_sealed() -> None:
    r = TestClient(app).post("/api/demo/replay_injection", auth=AUTH).json()
    assert r["decision"]["outcome"] == "deny"
    assert find(kind="decision", subject_id="INV-0007")


def test_tamper_then_reset() -> None:
    cl = TestClient(app)
    cl.post("/api/demo/replay_injection", auth=AUTH)
    r = cl.post("/api/demo/tamper", auth=AUTH).json()
    assert r["verify"]["ok"] is False and r["verify"]["broken_at"] == r["tampered_id"]
    cl.post("/api/demo/reset", auth=AUTH)
    assert cl.get("/api/ledger/verify", auth=AUTH).json()["ok"]


def test_scam_email_runs_sentinel() -> None:
    cl = TestClient(app)
    assert cl.post("/api/demo/scam_email", auth=AUTH).json()["ok"]
    assert cl.get("/api/runs", auth=AUTH).json()[0]["agent"] == "sentinel"


def test_inbox_returns_verdict() -> None:
    r = TestClient(app).post("/api/inbox", auth=AUTH, json={
        "from": "service@paypa1-support.com", "subject": "Payment received",
        "body": "You have received $600.00 for INV-0007.", "invoice_id": "INV-0007"}).json()
    assert r["run_id"] and r["verdict"]["verdict"] == "scam"


def test_reset_seeds_story_for_every_screen() -> None:
    cl = TestClient(app)
    cl.post("/api/demo/reset", auth=AUTH)
    [d] = cl.get("/api/disputes", auth=AUTH).json()
    assert (d["id"], d["amount_cents"], d["buyer_name"]) == ("PP-D-12345", 60000, "Alex M.")
    detail = cl.get("/api/disputes/PP-D-12345", auth=AUTH).json()
    assert detail["evidence_pack"]["recommended_action"] == "provide_evidence"
    assert detail["approval_id"]
    inv = {i["id"]: i for i in cl.get("/api/invoices", auth=AUTH).json()}
    assert inv["INV-0007"]["status"] == "paid" and inv["INV-0007"]["shipped"]
    assert inv["INV-0006"]["status"] == "overdue" and inv["INV-0006"]["days_overdue"] == 5
    assert cl.post("/api/shipments", auth=AUTH, json={"invoice_id": "INV-0005", "tracking_number": "T1"}).json()["sealed"]
    assert {i["id"]: i for i in cl.get("/api/invoices", auth=AUTH).json()}["INV-0005"]["shipped"]
    assert 0 <= cl.get("/api/health", auth=AUTH).json()["score"] <= 100
