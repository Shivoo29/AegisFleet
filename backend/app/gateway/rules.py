"""Gateway rule tables (M6). Frozen — change only via PR approved by SKJ."""

# Tools each agent is allowed to call at all.
ALLOW = {
    "collector": {"get_invoice", "list_invoices", "send_invoice_reminder"},
    "sentinel": {"get_invoice", "list_invoices", "list_transactions"},
    "guardian": {
        "create_shipment_tracking",
        "get_shipment_tracking",
        "update_shipment_tracking",
    },
    "defender": {
        "list_disputes",
        "get_dispute",
        "send_dispute_message",
        "provide_dispute_evidence",
        "make_dispute_offer",
        "accept_dispute_claim",
    },
    # Any outside AI agent (Claude, ChatGPT, a buyer's shopping agent) connected over MCP.
    # It can bill and refund, never touch disputes, and money only goes back to the buyer of record.
    "external": {"get_invoice", "create_invoice", "send_invoice", "send_invoice_reminder", "refund_invoice"},
}

# Tools that move money out of the seller's account. Only these trip the amount threshold.
MONEY_OUT = {"refund_invoice", "create_refund", "make_dispute_offer"}

# Tools that always require a human approval before execution.
ALWAYS_APPROVE = {
    "provide_dispute_evidence",
    "make_dispute_offer",
    "accept_dispute_claim",
}

# Records seeded by the demo story (app/demo.py seed()). PayPal has never heard of them, so calls
# about them run on the fake client and are sealed as simulated. Everything else hits the sandbox.
SIMULATED_IDS = {"INV-0005", "INV-0006", "INV-0007", "PP-D-12345", "CAP-DEMO"}


def is_simulated(args: dict) -> bool:
    return any(args.get(k) in SIMULATED_IDS for k in ("invoice_id", "dispute_id", "capture_id", "subject_id"))


# Per (agent, tool) cap: max executions per subject per 7-day window.
CAPS = {("collector", "send_invoice_reminder"): 2, ("external", "send_invoice_reminder"): 2,
        ("external", "refund_invoice"): 1}


def needs_approval(agent: str, tool: str, args: dict) -> bool:
    """Return True when this call must be held for a human."""
    from app.config import get_settings
    if tool in ALWAYS_APPROVE:
        return True
    amount = args.get("amount_cents")
    if tool in MONEY_OUT and isinstance(amount, int) and amount >= get_settings().approval_threshold_cents:
        return True
    if tool == "send_dispute_message":  # first message on a dispute goes past a human
        return not _done_before(agent, tool, args.get("dispute_id"))
    # ponytail: "first reminder to a new client" rule skipped; add when Collector tracks clients.
    return False


def _done_before(agent: str, tool: str, subject_id) -> bool:
    from app.db import conn
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM ledger WHERE kind='decision' AND subject_id=%s "
                "AND payload->>'agent'=%s AND payload->>'tool'=%s AND payload->>'outcome'='allow' LIMIT 1",
                (str(subject_id), agent, tool))
            return cur.fetchone() is not None


def validate(agent: str, tool: str, args: dict) -> str | None:
    """Return an error string if args are invalid, else None."""
    amount = args.get("amount_cents")
    if amount is not None and (not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0):
        return "amount_cents must be a positive integer"
    if tool in ("get_invoice", "send_invoice_reminder") and not args.get("invoice_id"):
        return "invoice_id required"
    if tool in ALLOW["defender"] - {"list_disputes"} and not args.get("dispute_id"):
        return "dispute_id required"
    if tool == "create_invoice" and (amount is None or amount > 500_000):
        return "amount_cents required, at most 500000"
    if tool == "refund_invoice":
        paid, left = refundable_cents(args.get("subject_id"))
        if amount is None:
            return "amount_cents required"
        if paid <= 0:
            return "no verified PayPal payment on this invoice to refund"
        if left <= 0:
            return "already refunded in full, or a refund is waiting for the seller's approval"
        if amount > left:
            return f"refund exceeds what the buyer paid (at most {left} cents left)"
    disputed = args.get("disputed_amount_cents")
    if tool == "make_dispute_offer" and amount is not None and disputed is not None and amount > disputed:
        return "offer exceeds disputed amount"
    return None


def refundable_cents(subject_id) -> tuple[int, int]:
    """(paid, still refundable) in cents: verified PayPal payments on this invoice minus refunds executed
    or waiting for approval. The ledger is the source of truth, not what an agent claims."""
    from app.db import conn
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(
                "SELECT COALESCE(MAX((payload->>'amount_cents')::bigint), 0) AS paid FROM ledger WHERE kind='event' "
                "AND subject_id=%s AND payload->>'verified'='true' "
                "AND payload->>'type' IN ('invoice.paid','payment.captured')", (str(subject_id),))
            paid = int(cur.fetchone()["paid"])
            # executed refunds, plus held ones still waiting (so two requests can't both pass the check)
            cur.execute(
                "SELECT COALESCE(SUM((payload->'args'->>'amount_cents')::bigint), 0) AS out FROM ledger "
                "WHERE kind='decision' AND subject_id=%s AND payload->>'tool' IN ('refund_invoice','create_refund') "
                "AND payload->>'outcome'='allow'", (str(subject_id),))
            done = int(cur.fetchone()["out"])
            cur.execute(
                "SELECT COALESCE(SUM(amount_cents), 0) AS held FROM approvals WHERE status='pending' "
                "AND tool IN ('refund_invoice','create_refund') AND args->>'subject_id'=%s", (str(subject_id),))
            return paid, paid - done - int(cur.fetchone()["held"])


def is_allowed(agent: str, tool: str) -> bool:
    return tool in ALLOW.get(agent, set())


def agent_enabled(agent: str) -> bool:
    from app.config import get_settings
    s = get_settings()
    return agent in s.agents_enabled or (agent == "external" and s.external_agents_enabled)


def kill_switch_active() -> bool:
    from app.config import get_settings
    if get_settings().kill_switch:
        return True
    from app.db import conn
    try:
        with conn() as c:
            with c.cursor() as cur:
                cur.execute("SELECT value FROM settings WHERE key = %s", ("kill_switch",))
                row = cur.fetchone()
        return bool(row and row["value"].lower() in ("1", "true", "yes", "on"))
    except Exception:
        return True  # fail closed: if we can't read the switch, nothing moves