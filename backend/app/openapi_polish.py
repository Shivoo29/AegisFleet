"""Post-process the generated OpenAPI spec for SDK generators and API linters (APIMatic).

- Field and parameter descriptions come from one glossary, since the same names recur across schemas.
- Per-property titles ("Id", "Status") are dropped: linters flag them as duplicates. Component schema
  titles stay; SDK generators name their types from them.
"""

FIELDS = {
    "action": "approve or reject",
    "agent": "Agent name: sentinel, defender, guardian or collector",
    "amount_cents": "Amount in minor units (cents)",
    "appeal_pack": "Draft appeal text Guardian wrote for PayPal, if the account is limited",
    "approval_id": "Id of the pending approval for this action",
    "args": "Tool arguments the agent asked the gateway to run",
    "body": "Email body text",
    "broken_at": "First ledger id whose hash no longer matches; null when the chain is intact",
    "buyer_email": "Buyer's email address",
    "buyer_name": "Buyer's name as PayPal reports it",
    "carrier": "Shipping carrier, e.g. UPS",
    "chain_ok": "True when every ledger hash still matches",
    "checked": "Number of ledger entries checked",
    "created_at": "When it was created (ISO 8601)",
    "currency": "ISO 4217 currency code",
    "days_overdue": "Days past the due date; 0 when paid or not yet due",
    "decision": "Gateway decision for the executed action",
    "detail": "Validation errors",
    "dispute": "The dispute",
    "dispute_id": "PayPal dispute id, e.g. PP-D-12345",
    "due_by": "Seller response deadline (ISO 8601)",
    "event_type": "Event that started the run, e.g. dispute.created",
    "evidence_pack": "Defender's evidence pack; every fact cites a ledger id",
    "factors": "What the health score is made of",
    "from": "Sender address",
    "hash": "SHA-256 of this entry plus the previous hash",
    "health_score": "Account health score, 0-100",
    "id": "Unique id",
    "impact": "How this factor moves the score",
    "invoice_id": "Invoice id, e.g. INV-0007",
    "kill_switch": "True when the kill switch blocks all agent actions",
    "kind": "Entry kind: event, decision, agent_step, approval or note",
    "ledger_entry_id": "Ledger entry that seals this",
    "limit": "Maximum number of items to return",
    "loc": "Where the invalid value is",
    "message": "What happened, in plain words",
    "money_at_risk_cents": "Total held for approval, in cents",
    "msg": "Error message",
    "name": "Factor name",
    "note": "Free-text note",
    "ok": "True on success",
    "on": "True when the kill switch is on",
    "open_disputes": "Number of open disputes",
    "outcome": "allow, hold or deny",
    "output": "Agent's structured result",
    "overdue_invoices": "Number of overdue invoice events",
    "paid_at": "When payment was verified (ISO 8601)",
    "password": "Console password",
    "pay_url": "PayPal payment page for this invoice",
    "payload": "Sealed data for this entry",
    "pending_approvals": "Actions waiting for a human",
    "prev_hash": "Hash of the previous entry; empty for the first",
    "reason": "Why",
    "recommendations": "Steps that would raise the score",
    "result": "What the executed tool returned",
    "risk": "Payment risk: low, medium or high",
    "role": "dev (seller) or judge",
    "run_id": "Agent run id",
    "score": "Health score, 0-100",
    "sealed": "True once the event is in the ledger",
    "shipped": "True when tracking was added",
    "started_at": "When the run started (ISO 8601)",
    "status": "Current status",
    "steps": "Each step the agent took",
    "subject": "Email subject",
    "subject_id": "What this is about: an invoice, dispute or email id",
    "summary": "One-line summary",
    "tool": "Gateway tool the agent called",
    "tracking_number": "Carrier tracking number",
    "type": "Error type",
    "user": "Logged-in user name",
    "username": "dev or judge",
    "value": "Measured value",
    "verdict": "Sentinel verdict: scam, legit or unsure, with red flags",
}


def _prop(schema: dict, name: str) -> None:
    schema.pop("title", None)
    schema.setdefault("description", FIELDS.get(name, name.replace("_", " ").capitalize()))
    for alt in schema.get("anyOf", []):
        alt.setdefault("description", "Not set" if alt.get("type") == "null" else schema["description"])


def polish(spec: dict) -> dict:
    spec["info"]["contact"] = {"name": "AegisFleet team", "url": "https://github.com/Shivoo29/aegisfleet"}
    for s in spec.get("servers", []):
        s.setdefault("x-environment", "production")
    for name, s in spec["components"]["schemas"].items():
        s.setdefault("description", f"{name} object")
        for pname, p in s.get("properties", {}).items():
            _prop(p, pname)
    for path in spec["paths"].values():
        for op in path.values():
            op.setdefault("tags", ["ops"])
            for prm in op.get("parameters", []):
                prm.setdefault("description", FIELDS.get(prm["name"], prm["name"]))
                _prop(prm["schema"], prm["name"])
    return spec
