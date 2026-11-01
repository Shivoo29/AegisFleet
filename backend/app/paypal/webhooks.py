"""PayPal webhook endpoint (M5)."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/webhooks/paypal")
async def paypal_webhook() -> dict:
    # TODO(SKJ): verify signature, dedupe on paypal_event_id, map type,
    # store_event, then BackgroundTasks.add_task(route, event).
    return {"ok": True}