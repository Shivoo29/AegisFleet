#!/usr/bin/env python3
"""Replay a webhook JSON file to local API."""
import sys
import json
import httpx

if len(sys.argv) < 2:
    print("usage: python -m scripts.replay <json file>")
    sys.exit(1)

with open(sys.argv[1], "r", encoding="utf-8") as f:
    body = json.load(f)

r = httpx.post("http://localhost:8000/webhooks/paypal", json=body, timeout=10)
print(r.status_code, r.json())