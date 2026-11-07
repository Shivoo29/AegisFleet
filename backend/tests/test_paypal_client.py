"""M4 PayPal client: token refresh on 401, idempotency header, cents -> string."""
import json

import httpx

from app.paypal.client import PayPalClient


def test_refresh_on_401_and_request_id() -> None:
    seen, tokens = [], iter(["t1", "t2"])

    def handler(req: httpx.Request) -> httpx.Response:
        if req.url.path == "/v1/oauth2/token":
            return httpx.Response(200, json={"access_token": next(tokens), "expires_in": 3600})
        seen.append(req)
        if req.headers["authorization"] == "Bearer t1":
            return httpx.Response(401)
        return httpx.Response(201, json={"ok": True})

    c = PayPalClient(http=httpx.Client(base_url="https://x", transport=httpx.MockTransport(handler)))
    out = c.make_dispute_offer({"dispute_id": "PP-D-1", "amount_cents": 60000, "currency": "USD"})
    assert out == {"ok": True}
    assert [r.headers["authorization"] for r in seen] == ["Bearer t1", "Bearer t2"]
    assert seen[0].headers["paypal-request-id"] == seen[1].headers["paypal-request-id"]
    assert json.loads(seen[1].content)["offer_amount"] == {"currency_code": "USD", "value": "600.00"}
