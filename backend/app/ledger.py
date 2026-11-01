"""Proof Ledger (M3). Hash-chained, append-only."""
import hashlib
import json
from datetime import datetime, timezone

from app.db import conn
from app.models import LedgerEntry

GENESIS = "0" * 64
_LOCK_KEY = 42


def _canonical(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _iso(dt: datetime) -> str:
    # psycopg returns timestamptz in the session time zone; normalise so the hash is stable
    return dt.astimezone(timezone.utc).isoformat()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def seal(kind: str, subject_id: str, summary: str, payload: dict) -> LedgerEntry:
    """Append one entry atomically under a pg advisory lock."""
    created_at = _now()
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT pg_advisory_xact_lock(%s)", (_LOCK_KEY,))
            cur.execute(
                "SELECT hash FROM ledger ORDER BY id DESC LIMIT 1"
            )
            row = cur.fetchone()
            prev_hash = row["hash"] if row else GENESIS
            payload_obj = dict(payload)
            entry_obj = {
                "kind": kind,
                "subject_id": subject_id,
                "summary": summary,
                "payload": payload_obj,
                "created_at": _iso(created_at),
            }
            digest = hashlib.sha256(
                (prev_hash + _canonical(entry_obj)).encode("utf-8")
            ).hexdigest()
            cur.execute(
                "INSERT INTO ledger (kind, subject_id, summary, payload, prev_hash, hash, created_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id, kind, subject_id, summary, payload, prev_hash, hash, created_at",
                (kind, subject_id, summary, json.dumps(payload_obj), prev_hash, digest, created_at),
            )
            r = cur.fetchone()
        c.commit()
    return LedgerEntry(
        id=r["id"], kind=r["kind"], subject_id=r["subject_id"], summary=r["summary"],
        payload=r["payload"], prev_hash=r["prev_hash"], hash=r["hash"], created_at=r["created_at"],
    )


def verify() -> dict:
    """Walk by id ascending, recompute every hash. Return {ok, checked, broken_at}."""
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "SELECT id, kind, subject_id, summary, payload, prev_hash, hash, created_at "
                "FROM ledger ORDER BY id ASC"
            )
            rows = cur.fetchall()
    prev = GENESIS
    checked = 0
    for r in rows:
        checked += 1
        entry_obj = {
            "kind": r["kind"],
            "subject_id": r["subject_id"],
            "summary": r["summary"],
            "payload": r["payload"],
            "created_at": _iso(r["created_at"]),
        }
        digest = hashlib.sha256(
            (prev + _canonical(entry_obj)).encode("utf-8")
        ).hexdigest()
        if digest != r["hash"]:
            return {"ok": False, "checked": checked, "broken_at": r["id"]}
        prev = r["hash"]
    return {"ok": True, "checked": checked, "broken_at": None}


def find(kind: str | None = None, subject_id: str | None = None, limit: int = 100, **payload_eq) -> list[LedgerEntry]:
    """Newest first. payload_eq filters on top-level payload keys (JSONB)."""
    where = []
    params: list = []
    if kind is not None:
        where.append("kind = %s")
        params.append(kind)
    if subject_id is not None:
        where.append("subject_id = %s")
        params.append(subject_id)
    for k, v in payload_eq.items():
        where.append("payload->>%s = %s")
        params.append(k)
        params.append(str(v))
    sql = (
        "SELECT id, kind, subject_id, summary, payload, prev_hash, hash, created_at "
        "FROM ledger"
    )
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id DESC LIMIT %s"
    params.append(limit)
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
    out = []
    for r in rows:
        out.append(LedgerEntry(
            id=r["id"], kind=r["kind"], subject_id=r["subject_id"], summary=r["summary"],
            payload=r["payload"], prev_hash=r["prev_hash"], hash=r["hash"], created_at=r["created_at"],
        ))
    return out