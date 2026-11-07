"""Console API (M8). HTTP Basic behind /api/*."""
import secrets
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import get_settings
from app.db import conn
from app.ledger import find as ledger_find, verify

router = APIRouter(prefix="/api")
security = HTTPBasic()


def _basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    settings = get_settings()
    if not secrets.compare_digest(credentials.password, settings.console_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid console password",
            headers={"WWW-Authenticate": "Basic"},
        )


@router.get("/summary", dependencies=[Depends(_basic_auth)])
def summary() -> dict:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS n FROM approvals WHERE status='pending'")
            pending = cur.fetchone()["n"]
            cur.execute(
                "SELECT COALESCE(SUM(amount_cents),0) AS s FROM approvals WHERE status='pending'"
            )
            money = int(cur.fetchone()["s"])
            cur.execute("SELECT COUNT(*) AS n FROM events WHERE type LIKE 'dispute%' AND rejected=false")
            disputes = cur.fetchone()["n"]
            cur.execute("SELECT COUNT(*) AS n FROM events WHERE type='invoice.overdue'")
            overdue = cur.fetchone()["n"]
    v = verify()
    from app.gateway.rules import kill_switch_active
    return {
        "money_at_risk_cents": money,
        "currency": "USD",
        "pending_approvals": pending,
        "open_disputes": disputes,
        "overdue_invoices": overdue,
        "health_score": 82,
        "kill_switch": kill_switch_active(),
        "chain_ok": v["ok"],
    }


@router.get("/ledger", dependencies=[Depends(_basic_auth)])
def ledger(kind: str | None = None, subject_id: str | None = None, limit: int = 100) -> list:
    return [e.model_dump() for e in ledger_find(kind=kind, subject_id=subject_id, limit=limit)]


@router.get("/ledger/verify", dependencies=[Depends(_basic_auth)])
def ledger_verify() -> dict:
    return verify()


@router.get("/approvals", dependencies=[Depends(_basic_auth)])
def approvals(status: str = "pending") -> list:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "SELECT id, agent, tool, args, reason, summary, amount_cents, currency, status, created_at "
                "FROM approvals WHERE status=%s ORDER BY created_at DESC", (status,)
            )
            rows = cur.fetchall()
    return rows


@router.post("/approvals/{approval_id}/{action}", dependencies=[Depends(_basic_auth)])
def decide_approval(approval_id: str, action: str, body: dict | None = None,
                    credentials: HTTPBasicCredentials = Depends(security)) -> dict:
    from app.gateway import gateway
    if action not in ("approve", "reject"):
        raise HTTPException(404, "action must be approve or reject")
    note = (body or {}).get("note", "")
    try:
        if action == "reject":
            gateway.reject(approval_id, credentials.username, note)
            return {"status": "rejected"}
        d = gateway.approve(approval_id, credentials.username, note)
    except KeyError:
        raise HTTPException(409, "approval not found or already decided")
    return {"status": "approved", "decision": d.model_dump()}


@router.get("/runs", dependencies=[Depends(_basic_auth)])
def runs(limit: int = 20) -> list:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "SELECT id, agent, event_type, status, steps, output, started_at "
                "FROM agent_runs ORDER BY started_at DESC LIMIT %s", (limit,)
            )
            rows = cur.fetchall()
    return rows


@router.get("/killswitch", dependencies=[Depends(_basic_auth)])
def get_killswitch() -> dict:
    from app.gateway.rules import kill_switch_active
    return {"on": kill_switch_active()}


@router.post("/killswitch", dependencies=[Depends(_basic_auth)])
def post_killswitch(body: dict) -> dict:
    val = "true" if body.get("on") else "false"
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "INSERT INTO settings (key, value) VALUES ('kill_switch', %s) "
                "ON CONFLICT (key) DO UPDATE SET value=%s",
                (val, val),
            )
        c.commit()
    return {"on": val == "true"}


@router.post("/inbox", dependencies=[Depends(_basic_auth)])
def inbox(body: dict, background_tasks: BackgroundTasks) -> dict:
    from app.events import route, store_event
    from app.models import Event
    ev = Event(
        id=str(uuid4()),
        type="email.received",
        source="inbox",
        subject_id=body.get("subject_id", body.get("invoice_id", "test")),
        data=body,
        verified=False,
        received_at=datetime.now(timezone.utc),
    )
    store_event(ev)
    background_tasks.add_task(route, ev)
    return {"run_id": ev.id}


# TODO(SKJ): real data for the screens below.
@router.get("/disputes", dependencies=[Depends(_basic_auth)])
def disputes() -> list:
    return []


@router.get("/disputes/{dispute_id}", dependencies=[Depends(_basic_auth)])
def dispute_detail(dispute_id: str) -> dict:
    return {"dispute": {}, "evidence_pack": None, "approval_id": None}


@router.get("/invoices", dependencies=[Depends(_basic_auth)])
def invoices() -> list:
    return []


@router.post("/shipments", dependencies=[Depends(_basic_auth)])
def shipments(body: dict) -> dict:
    return {}


@router.get("/health", dependencies=[Depends(_basic_auth)])
def health() -> dict:
    return {}