"""PayPal gateway client (M4). Sandbox only; live is refused by config.

One method per gateway tool name. Args use our shapes (integer cents, our ids);
this file is the only place that knows PayPal URLs and "600.00" money strings.
"""
import json
import time
import uuid

import httpx

from app.config import get_settings

SANDBOX = "https://api-m.sandbox.paypal.com"


def _cents_to_str(cents) -> str:
    """Money = integer cents; '600.00' strings only here."""
    return f"{int(cents) / 100:.2f}"


def _money(args: dict) -> dict:
    return {"currency_code": args.get("currency", "USD"), "value": _cents_to_str(args["amount_cents"])}


class PayPalClient:
    def __init__(self, http: httpx.Client | None = None) -> None:
        self.settings = get_settings()
        self._token: str | None = None
        self._token_expires_at: float = 0.0
        self._http = http or httpx.Client(base_url=SANDBOX, timeout=10)

    # --- plumbing ---
    def _auth(self, force: bool = False) -> str:
        if force or not self._token or time.time() > self._token_expires_at - 60:
            r = self._http.post("/v1/oauth2/token", data={"grant_type": "client_credentials"},
                                auth=(self.settings.paypal_client_id, self.settings.paypal_client_secret))
            r.raise_for_status()
            d = r.json()
            self._token, self._token_expires_at = d["access_token"], time.time() + d["expires_in"]
        return self._token

    def _req(self, method: str, path: str, **kw) -> dict:
        headers = kw.pop("headers", {})
        if method != "GET":  # idempotency: a retried POST never double-acts
            headers["PayPal-Request-Id"] = str(uuid.uuid4())
        for attempt in (1, 2):
            headers["Authorization"] = f"Bearer {self._auth(force=attempt == 2)}"
            r = self._http.request(method, path, headers=headers, **kw)
            if r.status_code != 401:
                break
        r.raise_for_status()
        return r.json() if r.content else {}

    # --- invoices ---
    def get_invoice(self, args: dict) -> dict:
        return self._req("GET", f"/v2/invoicing/invoices/{args['invoice_id']}")

    def list_invoices(self, args: dict) -> dict:
        return self._req("GET", "/v2/invoicing/invoices", params={"page_size": args.get("page_size", 50)})

    def create_invoice(self, args: dict) -> dict:
        """One-line invoice from our shape: invoice_number, item, amount_cents, currency, note."""
        body = {"detail": {"invoice_number": args["invoice_number"], "currency_code": args.get("currency", "USD"),
                           "note": args.get("note", "")},
                "items": [{"name": args.get("item", "Order"), "quantity": "1", "unit_amount": _money(args)}]}
        if args.get("business_name"):
            body["invoicer"] = {"business_name": args["business_name"]}
        if args.get("buyer_email"):
            body["primary_recipients"] = [{"billing_info": {"email_address": args["buyer_email"]}}]
        out = self._req("POST", "/v2/invoicing/invoices", json=body)
        out.setdefault("id", out.get("href", "").rstrip("/").split("/")[-1])  # minimal response: id is in the link
        return out

    def send_invoice(self, args: dict) -> dict:
        """Without a buyer email PayPal still issues the invoice; the payer-view link is shareable."""
        return self._req("POST", f"/v2/invoicing/invoices/{args['invoice_id']}/send",
                         json={"send_to_recipient": bool(args.get("buyer_email")), "send_to_invoicer": False})

    def record_invoice_payment(self, args: dict) -> dict:
        """Seller records a payment received outside PayPal checkout; PayPal still fires INVOICING.INVOICE.PAID."""
        return self._req("POST", f"/v2/invoicing/invoices/{args['invoice_id']}/payments",
                         json={"method": args.get("method", "OTHER"), "amount": _money(args), "note": args.get("note", "")})

    def send_invoice_reminder(self, args: dict) -> dict:
        return self._req("POST", f"/v2/invoicing/invoices/{args['invoice_id']}/remind",
                         json={"subject": args.get("subject", "Payment reminder"), "note": args.get("note", "")})

    # --- payments ---
    def list_transactions(self, args: dict) -> dict:
        # PayPal caps the window at 31 days; caller passes ISO start/end or gets the last 30 days.
        end = args.get("end_date") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        start = args.get("start_date") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 30 * 86400))
        return self._req("GET", "/v1/reporting/transactions",
                         params={"start_date": start, "end_date": end, "fields": "all"})

    def create_refund(self, args: dict) -> dict:
        body = {"amount": _money(args)} if args.get("amount_cents") else {}
        return self._req("POST", f"/v2/payments/captures/{args['capture_id']}/refund", json=body)

    # --- shipment tracking ---
    def create_shipment_tracking(self, args: dict) -> dict:
        return self._req("POST", "/v1/shipping/trackers-batch", json={"trackers": [{
            "transaction_id": args["transaction_id"], "tracking_number": args["tracking_number"],
            "status": args.get("status", "SHIPPED"), "carrier": args.get("carrier", "OTHER")}]})

    def get_shipment_tracking(self, args: dict) -> dict:
        return self._req("GET", f"/v1/shipping/trackers/{args['transaction_id']}-{args['tracking_number']}")

    def update_shipment_tracking(self, args: dict) -> dict:
        return self._req("PUT", f"/v1/shipping/trackers/{args['transaction_id']}-{args['tracking_number']}", json={
            "transaction_id": args["transaction_id"], "tracking_number": args["tracking_number"],
            "status": args["status"], "carrier": args.get("carrier", "OTHER")})

    # --- disputes ---
    def list_disputes(self, args: dict) -> dict:
        return self._req("GET", "/v1/customer/disputes", params={"page_size": args.get("page_size", 20)})

    def get_dispute(self, args: dict) -> dict:
        return self._req("GET", f"/v1/customer/disputes/{args['dispute_id']}")

    def send_dispute_message(self, args: dict) -> dict:
        return self._req("POST", f"/v1/customer/disputes/{args['dispute_id']}/send-message",
                         json={"message": args["message"]})

    def provide_dispute_evidence(self, args: dict) -> dict:
        # ponytail: notes-only evidence (no file uploads); add document parts when we attach PDFs.
        evidence = {"evidences": [{"evidence_type": args.get("evidence_type", "OTHER"),
                                   "notes": args.get("note", "")}]}
        return self._req("POST", f"/v1/customer/disputes/{args['dispute_id']}/provide-evidence",
                         files={"input": (None, json.dumps(evidence), "application/json")})

    def make_dispute_offer(self, args: dict) -> dict:
        return self._req("POST", f"/v1/customer/disputes/{args['dispute_id']}/make-offer", json={
            "note": args.get("note", ""), "offer_amount": _money(args), "offer_type": args.get("offer_type", "REFUND")})

    def accept_dispute_claim(self, args: dict) -> dict:
        return self._req("POST", f"/v1/customer/disputes/{args['dispute_id']}/accept-claim",
                         json={"note": args.get("note", "")})

    # --- webhooks ---
    def verify_webhook_signature(self, args: dict) -> dict:
        return self._req("POST", "/v1/notifications/verify-webhook-signature", json=args)


_client: PayPalClient | None = None


def get_client():
    settings = get_settings()
    if settings.paypal_mode == "fake":
        from app.paypal.fake import FakePayPal
        return FakePayPal()
    global _client
    if _client is None:  # one client so the OAuth token is reused across calls
        _client = PayPalClient()
    return _client
