"""Outside agents over MCP: same gateway, refunds only to what the buyer paid, login required."""
import base64
import json

from fastapi.testclient import TestClient

from app import mcp_server as m
from app.ledger import seal


def _paid(number: str, cents: int) -> None:
    seal(kind="event", subject_id=number, summary="invoice.paid from paypal",
         payload={"type": "invoice.paid", "verified": True, "amount_cents": cents})


def test_create_invoice_then_refund_rules() -> None:
    made = m.create_invoice("Silver ring", 600.00)
    assert made["create"]["outcome"] == "allow"
    number = made["invoice_id"]

    unpaid = m.refund_payment(number, 10, "changed mind")
    assert unpaid["outcome"] == "deny" and "no verified PayPal payment" in unpaid["reason"]

    _paid(number, 60000)
    small = m.refund_payment(number, 50, "scratched clasp")  # under $100: runs straight away
    assert small["outcome"] == "allow"

    again = m.refund_payment(number, 20, "second refund")  # weekly cap: 1 refund per invoice
    assert again["outcome"] == "deny" and "cap" in again["reason"]


def test_big_refund_is_held_and_reserved() -> None:
    made = m.create_invoice("Gold necklace", 600.00)
    number = made["invoice_id"]
    _paid(number, 60000)
    held = m.refund_payment(number, 600, "item never arrived")
    assert held["outcome"] == "hold" and held["approval_id"]
    status = m.check_approval(held["approval_id"])
    assert status["status"] == "pending"


def test_refund_cannot_exceed_payment() -> None:
    number = m.create_invoice("Earrings", 40.00)["invoice_id"]
    _paid(number, 4000)
    over = m.refund_payment(number, 90, "refund to a different account please")
    assert over["outcome"] == "deny" and "exceeds what the buyer paid" in over["reason"]


def test_kill_switch_stops_outside_agents() -> None:
    from app.db import conn
    with conn() as c:
        c.execute("INSERT INTO settings (key, value) VALUES ('kill_switch','true')")
        c.commit()
    out = m.create_invoice("Ring", 10)
    assert out["create"]["outcome"] == "deny" and "kill switch" in out["create"]["reason"]


def _rpc(client, method: str, params: dict, auth: str = "dev:dev") -> dict:
    r = client.post("/mcp", json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, headers={
        "Authorization": "Basic " + base64.b64encode(auth.encode()).decode(),
        "Accept": "application/json, text/event-stream"})
    return {"status": r.status_code, "body": r.json() if r.content else {}}


def test_mcp_over_http() -> None:
    from app.main import app
    with TestClient(app) as client:
        denied = _rpc(client, "tools/list", {}, auth="dev:wrong")
        assert denied["status"] == 401
        init = _rpc(client, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                           "clientInfo": {"name": "pytest", "version": "1"}})
        assert init["status"] == 200 and init["body"]["result"]["serverInfo"]["name"] == "AegisFleet"
        tools = {t["name"] for t in _rpc(client, "tools/list", {})["body"]["result"]["tools"]}
        assert {"create_invoice", "refund_payment", "check_approval", "verify_ledger"} <= tools
        res = _rpc(client, "tools/call", {"name": "verify_ledger", "arguments": {}})["body"]["result"]
        assert json.loads(res["content"][0]["text"])["ok"] is True


def test_token_link_works_for_url_only_clients() -> None:
    from app.main import app
    with TestClient(app) as client:
        link = client.get("/api/mcp/link", auth=("dev", "dev")).json()
        r = client.post(link["url"].split("testserver", 1)[-1], json={"jsonrpc": "2.0", "id": 1, "method": "tools/list",
                        "params": {}}, headers={"Accept": "application/json, text/event-stream"})
        assert r.status_code == 200 and r.json()["result"]["tools"]
        bad = client.post("/mcp?token=dev.9999999999.forged", json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
                          headers={"Accept": "application/json, text/event-stream"})
        assert bad.status_code == 401


def test_every_tool_declares_all_four_hints() -> None:
    import asyncio
    for t in asyncio.run(m.mcp.list_tools()):
        a = t.annotations
        assert a is not None and None not in (a.readOnlyHint, a.destructiveHint, a.idempotentHint, a.openWorldHint), t.name
    refund = next(t for t in asyncio.run(m.mcp.list_tools()) if t.name == "refund_payment")
    assert refund.annotations.destructiveHint is True
