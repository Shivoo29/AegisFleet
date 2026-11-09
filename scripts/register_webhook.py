#!/usr/bin/env python3
"""Register our webhook with PayPal (sandbox) and print its id for PAYPAL_WEBHOOK_ID.

From backend/: PYTHONPATH=. PAYPAL_MODE=sandbox .venv/bin/python ../scripts/register_webhook.py https://<host>/webhooks/paypal
"""
import sys

from app.paypal.client import get_client
from app.paypal.webhooks import TYPES

url = sys.argv[1]
c = get_client()
existing = [w for w in c._req("GET", "/v1/notifications/webhooks").get("webhooks", []) if w["url"] == url]
if existing:
    print(existing[0]["id"])
else:
    print(c._req("POST", "/v1/notifications/webhooks",
                 json={"url": url, "event_types": [{"name": t} for t in TYPES]})["id"])
