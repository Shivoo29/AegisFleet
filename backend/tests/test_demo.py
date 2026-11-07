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
    assert find() == []


def test_scam_email_runs_sentinel() -> None:
    cl = TestClient(app)
    assert cl.post("/api/demo/scam_email", auth=AUTH).json()["ok"]
    assert cl.get("/api/runs", auth=AUTH).json()[0]["agent"] == "sentinel"
