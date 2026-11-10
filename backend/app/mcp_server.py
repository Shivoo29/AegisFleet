"""AegisFleet over MCP: any AI agent (Claude Code, an assistant, a buyer's shopping agent) can bill,
remind and refund on PayPal, but only through the same gateway our own agents use.

Every money tool lands in gateway.call("external", ...): kill switch, allowlist, validation, weekly caps,
human approval for refunds of $100 or more, and a sealed ledger entry. Refunds can only go back to the
buyer of record, for no more than PayPal says they paid. There is no other path to PayPal.

Served at /mcp (streamable HTTP, stateless, JSON). Auth: HTTP Basic with a console login.
"""
import base64
import contextvars
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.responses import JSONResponse

INSTRUCTIONS = (
    "You are connected to AegisFleet, the guardrail gateway in front of a small PayPal seller's account "
    "(Riya's Jewellery, PayPal sandbox). You can issue invoices, send payment reminders, check whether a "
    "'payment received' email is real, and refund buyers. Every action passes AegisFleet's gateway and is "
    "sealed in a hash-chained ledger. Refunds of $100 or more wait for the seller to approve them in the "
    "console; use check_approval to follow up. A 'deny' is final: tell the user the reason, do not retry "
    "with different wording."
)

mcp = FastMCP("AegisFleet", instructions=INSTRUCTIONS)
_who = contextvars.ContextVar("mcp_who", default="mcp client")


# ---------- helpers ----------

def _rows(sql: str, args: tuple = ()) -> list:
    from app.db import conn
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(sql, args)
            return cur.fetchall()


def _call(tool: str, args: dict, why: str):
    from app.gateway import gateway
    return gateway.call("external", tool, args, f"{_who.get()}: {why}")


def _decision(d) -> dict:
    out = {"outcome": d.outcome, "reason": d.reason, "ledger_entry": d.ledger_entry_id}
    if d.approval_id:
        out["approval_id"] = d.approval_id
        out["next_step"] = ("Held for the seller. They approve or reject it in the AegisFleet console "
                            "(Approvals tab). Call check_approval with this id to see what happened.")
    if d.result:
        out["paypal_result"] = d.result
    return out


def _invoice(invoice_id: str) -> dict:
    """Our invoice number (AF-..., INV-0006) or PayPal's id -> gateway args for that invoice."""
    rows = _rows("SELECT id, data FROM invoices WHERE id=%s OR data->>'paypal_invoice_id'=%s",
                 (invoice_id, invoice_id))
    if not rows:
        raise ValueError(f"No invoice {invoice_id}. Call list_invoices to see the seller's invoices.")
    r = rows[0]
    return {"subject_id": r["id"], "invoice_id": r["data"].get("paypal_invoice_id") or r["id"],
            "currency": r["data"].get("currency", "USD")}


def _cents(amount_usd: float) -> int:
    return int(round(float(amount_usd) * 100))


# ---------- tools ----------

@mcp.tool()
def list_invoices() -> list:
    """The seller's invoices: amount, paid / overdue / refunded status, days overdue, PayPal payment link."""
    from app.api import invoices
    return invoices()


@mcp.tool()
def create_invoice(item: str, amount_usd: float, buyer_email: str = "") -> dict:
    """Issue a real PayPal (sandbox) invoice for one item and return its payment link.

    item: what the buyer is paying for, e.g. "Hand-made silver ring".
    amount_usd: price in US dollars, e.g. 45.00. At most $5,000.
    buyer_email: optional; PayPal emails the invoice to this address.
    """
    import json
    from app.db import conn
    number = f"AF-{datetime.now(timezone.utc):%m%d%H%M%S}"
    base = {"subject_id": number, "invoice_number": number, "item": item, "amount_cents": _cents(amount_usd),
            "currency": "USD", "business_name": "Riya's Jewellery", "buyer_email": buyer_email or None}
    made = _call("create_invoice", base, f"invoice {item} for ${amount_usd:.2f}")
    if made.outcome != "allow":
        return {"create": _decision(made)}
    pp_id = (made.result or {}).get("id") or number
    data = {"buyer_email": buyer_email or "sandbox buyer", "amount_cents": base["amount_cents"], "currency": "USD",
            "created_at": datetime.now(timezone.utc).isoformat(), "paypal_invoice_id": pp_id, "item": item,
            "created_by": _who.get()}
    with conn() as c:
        c.execute("INSERT INTO invoices (id, data) VALUES (%s,%s)", (number, json.dumps(data)))
        c.commit()
    sent = _call("send_invoice", {"subject_id": number, "invoice_id": pp_id, "buyer_email": buyer_email or None},
                 "issue the invoice to the buyer")
    pay_url = (sent.result or {}).get("href", "")
    if pay_url:
        with conn() as c:
            c.execute("UPDATE invoices SET data = data || %s::jsonb WHERE id=%s",
                      (json.dumps({"pay_url": pay_url}), number))
            c.commit()
    return {"invoice_id": number, "paypal_invoice_id": pp_id, "pay_url": pay_url,
            "create": _decision(made), "send": _decision(sent)}


@mcp.tool()
def send_payment_reminder(invoice_id: str, note: str = "") -> dict:
    """Send PayPal's payment reminder for an unpaid invoice. Capped at 2 per invoice per week."""
    return _decision(_call("send_invoice_reminder", {**_invoice(invoice_id), "note": note[:400]},
                           f"remind the buyer about {invoice_id}"))


@mcp.tool()
def refund_payment(invoice_id: str, amount_usd: float, reason: str) -> dict:
    """Refund the buyer of an invoice. The money can only go back to whoever paid it, and never more than
    PayPal says they paid. Refunds of $100 or more are held until the seller approves them."""
    return _decision(_call("refund_invoice", {**_invoice(invoice_id), "amount_cents": _cents(amount_usd),
                                              "note": reason[:255]}, f"refund ${amount_usd:.2f}: {reason}"))


@mcp.tool()
def check_approval(approval_id: str) -> dict:
    """Has the seller approved or rejected a held action yet, and what happened when it ran?"""
    rows = _rows("SELECT id, tool, status, args, decided_by, decided_at FROM approvals WHERE id=%s", (approval_id,))
    if not rows:
        return {"error": f"no approval {approval_id}"}
    a = rows[0]
    out = {"approval_id": a["id"], "tool": a["tool"], "status": a["status"], "decided_by": a["decided_by"]}
    ran = _rows("SELECT id, payload FROM ledger WHERE kind='decision' AND payload->>'approval_id'=%s "
                "AND payload->>'outcome'<>'hold' ORDER BY id DESC LIMIT 1", (approval_id,))
    if ran:
        out["result"] = {"outcome": ran[0]["payload"]["outcome"], "reason": ran[0]["payload"]["reason"],
                         "paypal_result": ran[0]["payload"].get("result"), "ledger_entry": ran[0]["id"]}
    return out


@mcp.tool()
def check_payment_email(sender: str, subject: str, body: str) -> dict:
    """Ask AegisFleet's Sentinel agent whether a 'you've been paid' email is real. It checks the email
    against verified PayPal payments in the ledger, not against what the email claims."""
    from app.api import inbox
    from app.schemas import InboxEmail
    return inbox(InboxEmail(**{"from": sender, "subject": subject, "body": body}))


@mcp.tool()
def get_history(invoice_id: str) -> list:
    """Every sealed ledger entry about an invoice or dispute, oldest first, with its hash."""
    from app.ledger import find
    return [{"id": e.id, "kind": e.kind, "summary": e.summary, "at": e.created_at.isoformat(), "hash": e.hash[:16]}
            for e in reversed(find(subject_id=invoice_id, limit=100))]


@mcp.tool()
def verify_ledger() -> dict:
    """Recompute the whole hash chain. ok=false names the first entry someone edited."""
    from app.ledger import verify
    return verify()


# ---------- transport ----------

def _user(header: str) -> str | None:
    from app.api import _role_for
    if not header.lower().startswith("basic "):
        return None
    try:
        name, _, pw = base64.b64decode(header[6:]).decode().partition(":")
    except Exception:  # noqa: BLE001
        return None
    return name if _role_for(name, pw) else None


class _Endpoint:
    """ASGI app for /mcp: console login check, then the MCP session manager."""
    manager: StreamableHTTPSessionManager | None = None

    async def __call__(self, scope, receive, send) -> None:
        headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}
        user = _user(headers.get("authorization", ""))
        if not user or self.manager is None:
            res = JSONResponse({"error": "login required: HTTP Basic with an AegisFleet console login"}, 401)
            await res(scope, receive, send)
            return
        client = headers.get("user-agent", "mcp client").split(" ")[0]
        token = _who.set(f"{client} ({user})")
        try:
            await self.manager.handle_request(scope, receive, send)
        finally:
            _who.reset(token)


endpoint = _Endpoint()


@asynccontextmanager
async def running():
    """A fresh session manager per app lifespan (each one can only run once)."""
    endpoint.manager = StreamableHTTPSessionManager(app=mcp._mcp_server, json_response=True, stateless=True)
    async with endpoint.manager.run():
        yield
    endpoint.manager = None
