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
}

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
CAPS = {("collector", "send_invoice_reminder"): 2}


def needs_approval(agent: str, tool: str, args: dict) -> bool:
    """Return True when this call must be held for a human."""
    from app.config import get_settings
    if tool in ALWAYS_APPROVE:
        return True
    amount = args.get("amount_cents")
    if isinstance(amount, int) and amount >= get_settings().approval_threshold_cents:
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
    disputed = args.get("disputed_amount_cents")
    if tool == "make_dispute_offer" and amount is not None and disputed is not None and amount > disputed:
        return "offer exceeds disputed amount"
    return None


def is_allowed(agent: str, tool: str) -> bool:
    return tool in ALLOW.get(agent, set())


def agent_enabled(agent: str) -> bool:
    from app.config import get_settings
    return agent in get_settings().agents_enabled


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