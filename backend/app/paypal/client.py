"""PayPal gateway client (M4). Only sandbox/fake at M0; live refused by config."""
from app.config import get_settings


def _cents_to_str(cents) -> str:
    """Money = integer cents; '600.00' strings only here."""
    return f"{int(cents) / 100:.2f}"


class PayPalClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._token: str | None = None
        self._token_expires_at: float = 0.0
        self._http = None  # httpx.AsyncClient created lazily

    # --- one stub per gateway tool name (LLD §6 table) ---
    def get_invoice(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def list_invoices(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def send_invoice_reminder(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def list_transactions(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def create_shipment_tracking(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def get_shipment_tracking(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def update_shipment_tracking(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def list_disputes(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def get_dispute(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def send_dispute_message(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def provide_dispute_evidence(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def make_dispute_offer(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def accept_dispute_claim(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def create_invoice(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def send_invoice(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def create_refund(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")

    def verify_webhook_signature(self, args: dict) -> dict:
        raise NotImplementedError("set at M0")


def get_client():
    settings = get_settings()
    if settings.paypal_mode == "fake":
        from app.paypal.fake import FakePayPal
        return FakePayPal()
    return PayPalClient()