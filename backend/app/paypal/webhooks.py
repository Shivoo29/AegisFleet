"""PayPal webhook endpoint (M5): verify, dedupe, map, store, route."""
import logging
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, BackgroundTasks, Request

from app.config import get_settings
from app.events import route, store_event
from app.models import Event

router = APIRouter(tags=["webhooks"])
log = logging.getLogger("aegis.webhooks")

# PayPal event_type -> our EventType. Anything else is acknowledged and ignored.
TYPES = {
    "INVOICING.INVOICE.PAID": "invoice.paid",
    "PAYMENT.CAPTURE.COMPLETED": "payment.captured",
    "PAYMENT.CAPTURE.REFUNDED": "payment.refunded",
    "CUSTOMER.DISPUTE.CREATED": "dispute.created",
    "CUSTOMER.DISPUTE.UPDATED": "dispute.updated",
    "CUSTOMER.DISPUTE.RESOLVED": "dispute.resolved",
}


def _cents(money: dict | None) -> tuple[int | None, str | None]:
    """PayPal {"value": "600.00", "currency_code": "USD"} -> (60000, "USD")."""
    if not money or "value" not in money:
        return None, None
    return int(Decimal(str(money["value"])) * 100), money.get("currency_code")


def normalize(body: dict) -> dict:
    """Pull subject, amount, currency and invoice id out of a PayPal webhook body."""
    r = body.get("resource") or {}
    kind = body.get("event_type", "")
    if kind.startswith("CUSTOMER.DISPUTE"):
        amount, ccy = _cents(r.get("dispute_amount"))
        txs = r.get("disputed_transactions") or [{}]
        invoice_id = txs[0].get("invoice_number")
        subject = r.get("dispute_id")
    elif kind.startswith("INVOICING.INVOICE"):
        inv = r.get("invoice") or r
        amount, ccy = _cents((inv.get("payments") or {}).get("paid_amount") or inv.get("amount"))
        invoice_id = (inv.get("detail") or {}).get("invoice_number") or inv.get("id")
        subject = invoice_id
    else:  # PAYMENT.CAPTURE.*: invoice_id is the merchant invoice number set on the order
        amount, ccy = _cents(r.get("amount"))
        invoice_id = r.get("invoice_id")
        subject = invoice_id or r.get("id")
    return {"id": body.get("id"), "paypal_type": kind, "subject_id": subject or "unknown",
            "invoice_id": invoice_id, "amount_cents": amount, "currency": ccy, "resource": r}


def _verified(request: Request, body: dict) -> bool:
    s = get_settings()
    if s.paypal_mode == "fake":
        return True
    from app.paypal.client import get_client
    h = request.headers
    try:
        out = get_client().verify_webhook_signature({
            "auth_algo": h.get("paypal-auth-algo"), "cert_url": h.get("paypal-cert-url"),
            "transmission_id": h.get("paypal-transmission-id"),
            "transmission_sig": h.get("paypal-transmission-sig"),
            "transmission_time": h.get("paypal-transmission-time"),
            "webhook_id": s.paypal_webhook_id, "webhook_event": body})
        return out.get("verification_status") == "SUCCESS"
    except Exception as e:  # noqa: BLE001 — can't verify means not verified
        log.warning("webhook verify failed: %s", e)
        return False


@router.post("/webhooks/paypal")
async def paypal_webhook(request: Request, background_tasks: BackgroundTasks) -> dict:
    body = await request.json()
    our_type = TYPES.get(body.get("event_type", ""))
    if not our_type or not body.get("id"):
        return {"ok": True, "ignored": True}
    data = normalize(body)
    event = Event(id=f"pp_{body['id']}", type=our_type, source="paypal", subject_id=data["subject_id"],
                  data=data, verified=_verified(request, body), received_at=datetime.now(timezone.utc))
    if not store_event(event):
        return {"ok": True, "duplicate": True}
    if event.verified:
        background_tasks.add_task(route, event)
    return {"ok": True}
