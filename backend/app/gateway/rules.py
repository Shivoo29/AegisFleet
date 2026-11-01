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

# Per (agent, tool) cap: max executions per subject per 7-day window.
CAPS = {("collector", "send_invoice_reminder"): 2}


def needs_approval(agent: str, tool: str, args: dict) -> bool:
    """Return True when this call must be held for a human."""
    return tool in ALWAYS_APPROVE


def validate(agent: str, tool: str, args: dict) -> str | None:
    """Return an error string if args are invalid, else None."""
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