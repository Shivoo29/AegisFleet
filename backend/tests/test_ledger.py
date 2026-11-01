"""M3 ledger tests: seal 3, tamper one, verify detects."""
import json

from app.db import conn
from app.ledger import find, seal, verify


def test_seal_and_verify() -> None:
    seal("event", "INV-1", "first", {"k": "v"})
    seal("event", "INV-2", "second", {"k": "v"})
    seal("event", "INV-3", "third", {"k": "v"})
    v = verify()
    assert v["ok"] is True
    assert v["checked"] == 3
    assert v["broken_at"] is None


def test_tamper_detected() -> None:
    seal("event", "INV-T", "tamper test", {"k": "v"})
    target = find(limit=10)[0]
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "UPDATE ledger SET payload = %s WHERE id = %s",
                (json.dumps({"k": "TAMPERED"}), target.id),
            )
        c.commit()
    v = verify()
    assert v["ok"] is False
    assert v["broken_at"] == target.id