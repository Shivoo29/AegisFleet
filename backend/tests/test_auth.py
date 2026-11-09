"""Console login: dev + judge sessions, bad logins, tampered cookies, Basic still works."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def _fresh_settings():
    from app.config import get_settings
    yield
    get_settings.cache_clear()  # don't leak JUDGE_PASSWORD into other tests


def _client(monkeypatch, judge: str = "judge-pass") -> TestClient:
    from app.config import get_settings
    monkeypatch.setenv("JUDGE_PASSWORD", judge)
    get_settings.cache_clear()
    return TestClient(app)


def test_dev_and_judge_login(monkeypatch) -> None:
    cl = _client(monkeypatch)
    assert cl.get("/api/summary").status_code == 401
    assert "www-authenticate" not in cl.get("/api/summary").headers  # no browser popup
    assert cl.post("/api/login", json={"username": "dev", "password": "dev"}).json()["role"] == "dev"
    assert cl.get("/api/summary").status_code == 200
    cl.post("/api/logout")
    assert cl.get("/api/summary").status_code == 401
    assert cl.post("/api/login", json={"username": "judge", "password": "judge-pass"}).json()["role"] == "judge"
    assert cl.get("/api/me").json() == {"user": "judge", "role": "judge"}


def test_bad_logins_rejected(monkeypatch) -> None:
    cl = _client(monkeypatch)
    for u, p in [("dev", "nope"), ("judge", "dev"), ("alice", "dev"), ("dev", "judge-pass")]:
        assert cl.post("/api/login", json={"username": u, "password": p}).status_code == 401, (u, p)
    assert _client(monkeypatch, judge="").post(
        "/api/login", json={"username": "judge", "password": ""}).status_code == 401  # judge off when unset


def test_tampered_cookie_rejected(monkeypatch) -> None:
    cl = _client(monkeypatch)
    cl.post("/api/login", json={"username": "judge", "password": "judge-pass"})
    user, exp, sig = cl.cookies.get("aegis_session").split("|")
    cl.cookies.set("aegis_session", f"dev|{exp}|{sig}")
    assert cl.get("/api/summary").status_code == 401


def test_basic_auth_still_works(monkeypatch) -> None:
    assert _client(monkeypatch).get("/api/summary", auth=("skj", "dev")).status_code == 200
