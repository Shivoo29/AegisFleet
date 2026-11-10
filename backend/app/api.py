"""Console API (M8). Session cookie (login page) or HTTP Basic behind /api/*."""
import hashlib
import hmac
import json
import secrets
import time
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import get_settings
from app.db import conn
from app.ledger import find as ledger_find, verify

router = APIRouter(prefix="/api")
security = HTTPBasic(auto_error=False)
COOKIE = "aegis_session"
SESSION_HOURS = 12


def _role_for(username: str, password: str) -> str | None:
    """'dev' with CONSOLE_PASSWORD, 'judge' with JUDGE_PASSWORD (if set). Constant-time compares."""
    s = get_settings()
    if username == "judge":
        return "judge" if s.judge_password and secrets.compare_digest(password, s.judge_password) else None
    return "dev" if secrets.compare_digest(password, s.console_password) else None


def _sign(payload: str) -> str:
    s = get_settings()
    # key changes when either password changes, which logs everyone out
    key = hashlib.sha256(f"aegis-session|{s.console_password}|{s.judge_password}".encode()).digest()
    return hmac.new(key, payload.encode(), hashlib.sha256).hexdigest()


def _session_user(token: str | None) -> str | None:
    try:
        user, exp, sig = (token or "").split("|")
        if hmac.compare_digest(sig, _sign(f"{user}|{exp}")) and int(exp) > time.time():
            return user
    except ValueError:
        pass
    return None


def _basic_auth(request: Request, credentials: HTTPBasicCredentials | None = Depends(security)) -> str:
    """Session cookie (console) or HTTP Basic (curl/tests). Returns the user name.

    No WWW-Authenticate header on 401, so browsers show our login page instead of a popup.
    """
    user = _session_user(request.cookies.get(COOKIE))
    if user:
        return user
    if credentials:
        role = _role_for(credentials.username, credentials.password)
        if role:
            return "judge" if role == "judge" else credentials.username
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="login required")


@router.post("/login")
def login(body: dict, request: Request, response: Response) -> dict:
    username, password = str(body.get("username", "")).strip(), str(body.get("password", ""))
    role = _role_for(username, password)
    if role is None or (role == "dev" and username != "dev"):
        time.sleep(0.5)  # ponytail: crude brute-force brake; per-IP lockout if this ever faces real users
        raise HTTPException(401, "wrong username or password")
    exp = int(time.time()) + SESSION_HOURS * 3600
    https = request.headers.get("x-forwarded-proto", request.url.scheme) == "https"
    response.set_cookie(COOKIE, f"{username}|{exp}|{_sign(f'{username}|{exp}')}", max_age=SESSION_HOURS * 3600,
                        httponly=True, secure=https, samesite="lax", path="/")
    return {"user": username, "role": role}


@router.post("/logout")
def logout(response: Response) -> dict:
    response.delete_cookie(COOKIE, path="/")
    return {"ok": True}


@router.get("/me")
def me(user: str = Depends(_basic_auth)) -> dict:
    return {"user": user, "role": "judge" if user == "judge" else "dev"}


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
        "health_score": health()["score"],
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
                    user: str = Depends(_basic_auth)) -> dict:
    from app.gateway import gateway
    if action not in ("approve", "reject"):
        raise HTTPException(404, "action must be approve or reject")
    note = (body or {}).get("note", "")
    try:
        if action == "reject":
            gateway.reject(approval_id, user, note)
            return {"status": "rejected"}
        d = gateway.approve(approval_id, user, note)
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
def inbox(body: dict) -> dict:
    """Run Sentinel inline (a few seconds) so the console gets the verdict in one call."""
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
    run = route(ev) or {}
    return {"run_id": run.get("run_id"), "status": run.get("status"), "verdict": run.get("output")}


def _rows(sql: str, args: tuple = ()) -> list:
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(sql, args)
            return cur.fetchall()


def _dispute_row(e: dict) -> dict:
    d, r = e["data"], e["data"].get("resource") or {}
    buyer = ((r.get("disputed_transactions") or [{}])[0].get("buyer") or {}).get("name")
    return {"id": e["subject_id"], "invoice_id": d.get("invoice_id"), "reason": r.get("reason", "UNKNOWN"),
            "status": r.get("status", "OPEN"), "amount_cents": d.get("amount_cents"),
            "currency": d.get("currency"), "buyer_name": buyer, "created_at": e["received_at"],
            "due_by": r.get("seller_response_due_date")}


def _latest_disputes() -> list:
    rows = _rows("SELECT DISTINCT ON (subject_id) subject_id, data, received_at FROM events "
                 "WHERE type LIKE 'dispute.%%' AND NOT rejected ORDER BY subject_id, received_at DESC")
    return sorted((_dispute_row(e) for e in rows), key=lambda d: d["created_at"], reverse=True)


@router.get("/disputes", dependencies=[Depends(_basic_auth)])
def disputes() -> list:
    return _latest_disputes()


@router.get("/disputes/{dispute_id}", dependencies=[Depends(_basic_auth)])
def dispute_detail(dispute_id: str) -> dict:
    found = [d for d in _latest_disputes() if d["id"] == dispute_id]
    if not found:
        raise HTTPException(404, "dispute not found")
    pack = _rows("SELECT output FROM agent_runs WHERE agent='defender' AND output->>'dispute_id'=%s "
                 "ORDER BY started_at DESC LIMIT 1", (dispute_id,))
    apr = _rows("SELECT id FROM approvals WHERE status='pending' AND args->>'dispute_id'=%s "
                "ORDER BY created_at DESC LIMIT 1", (dispute_id,))
    return {"dispute": found[0], "evidence_pack": pack[0]["output"] if pack else None,
            "approval_id": apr[0]["id"] if apr else None}


@router.get("/invoices", dependencies=[Depends(_basic_auth)])
def invoices() -> list:
    paid = {r["subject_id"]: r["created_at"] for r in _rows(
        "SELECT subject_id, min(created_at) AS created_at FROM ledger WHERE kind='event' "
        "AND payload->>'verified'='true' AND payload->>'type' IN ('payment.captured','invoice.paid') "
        "GROUP BY subject_id")}
    ships = {r["id"]: r["data"] for r in _rows("SELECT id, data FROM shipments")}
    plans = {r["output"]["invoice_id"]: r["output"] for r in _rows(
        "SELECT DISTINCT ON (output->>'invoice_id') output FROM agent_runs "
        "WHERE agent='collector' AND status='done' AND output ? 'invoice_id' "
        "ORDER BY output->>'invoice_id', started_at DESC")}
    today = datetime.now(timezone.utc).date()
    out = []
    for row in _rows("SELECT id, data FROM invoices ORDER BY id DESC"):
        d, inv = row["data"], row["id"]
        due = d.get("due_date")
        late = 0 if inv in paid or not due else max(0, (today - datetime.fromisoformat(due).date()).days)
        # Fallback until Collector has run for this invoice; then its deterministic plan wins.
        risk = "low" if inv in paid else "high" if late > 14 else "medium" if late else "low"
        plan = plans.get(inv) or {}
        out.append({"id": inv, "buyer_email": d.get("buyer_email"), "amount_cents": d.get("amount_cents"),
                    "currency": d.get("currency", "USD"),
                    "status": "paid" if inv in paid else "overdue" if late else "sent",
                    "days_overdue": late, "risk": plan.get("risk") or risk, "shipped": inv in ships,
                    "tracking_number": (ships.get(inv) or {}).get("tracking_number"),
                    "collector_tone": plan.get("tone"), "collector_next_action": plan.get("next_action"),
                    "created_at": d.get("created_at"), "paid_at": paid.get(inv), "pay_url": d.get("pay_url")})
    return out


@router.post("/shipments", dependencies=[Depends(_basic_auth)])
def shipments(body: dict) -> dict:
    """Seller adds tracking: store it, then fire shipment.created (sealed + routed to Guardian)."""
    from app.events import route, store_event
    from app.models import Event
    inv, tn = body.get("invoice_id"), body.get("tracking_number")
    if not inv or not tn:
        raise HTTPException(422, "invoice_id and tracking_number required")
    now = datetime.now(timezone.utc)
    data = {"invoice_id": inv, "tracking_number": tn, "carrier": body.get("carrier", "OTHER"),
            "shipped_at": now.isoformat()}
    with conn() as c:
        c.execute("INSERT INTO shipments (id, data) VALUES (%s,%s) ON CONFLICT (id) DO UPDATE "
                  "SET data=EXCLUDED.data, updated_at=now()", (inv, json.dumps(data)))
        c.commit()
    ev = Event(id=f"ship_{uuid4().hex[:8]}", type="shipment.created", source="console", subject_id=inv,
               data=data, verified=True, received_at=now)
    store_event(ev)
    run = route(ev) or {}
    return {"ok": True, "sealed": True, "run_id": run.get("run_id")}


@router.get("/health", dependencies=[Depends(_basic_auth)])
def health() -> dict:
    """Score and factors are recomputed from the ledger on every call, so a dispute that
    arrived after Guardian's last run still counts. Guardian's AI recommendations are
    reused only while the factors they were written for still hold."""
    from app.agents import guardian
    metrics, flags, factors = guardian._metrics(ledger_find(limit=1000))
    live = [f.model_dump() for f in factors]
    g = _rows("SELECT output FROM agent_runs WHERE agent='guardian' AND output ? 'score' "
              "ORDER BY started_at DESC LIMIT 1")
    last = g[0]["output"] if g else {}
    recs = last["recommendations"] if last.get("factors") == live else guardian._fallback_recommendations(flags)
    return {"score": guardian._score(metrics, flags), "factors": live,
            "recommendations": recs, "appeal_pack": last.get("appeal_pack")}
