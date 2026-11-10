"""Collector (P1): prioritize overdue invoices and draft a safe reminder."""
from __future__ import annotations

import json
import re
from datetime import date, datetime

from app.agents.base import AgentContext, load_prompt
from app.llm import LLMError
from app.models import CollectorPlan, Event, LedgerEntry

PAYMENT_TYPES = {"payment.captured", "invoice.paid"}
INVOICE_TYPES = {"invoice.sent", "invoice.overdue"}
REMINDER_TOOL = "send_invoice_reminder"
THREAT_RE = re.compile(
    r"\b(?:sue|lawsuit|legal action|court|police|collections?|garnish(?:ment)?|"
    r"late fee|penalt(?:y|ies)|report you|blacklist)\b",
    re.IGNORECASE,
)


def _payload(entry: LedgerEntry) -> dict:
    return entry.payload or {}


def _type(entry: LedgerEntry) -> str:
    return str(_payload(entry).get("type", "")).lower()


def _verified(entry: LedgerEntry) -> bool:
    return _payload(entry).get("verified") in (True, 1, "1", "true", "True")


def _invoice(entry: LedgerEntry) -> str:
    return str(_payload(entry).get("invoice_id") or entry.subject_id)


def _nested(event: Event) -> dict:
    invoice = event.data.get("invoice")
    return invoice if isinstance(invoice, dict) else {}


def _field(event: Event, key: str):
    nested = _nested(event)
    if key in nested and nested[key] is not None:
        return nested[key]
    return event.data.get(key)


def _int(value) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _day(value) -> date | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _money(amount_cents: int | None, currency: str) -> str:
    if amount_cents is None:
        return f"the outstanding balance ({currency})"
    return f"${amount_cents / 100:.2f} {currency}"


def _days_phrase(days: int) -> str:
    return "1 day" if days == 1 else f"{days} days"


def _days_overdue(event: Event, entries: list[LedgerEntry], invoice_id: str) -> int:
    for key in ("days_overdue", "overdue_days"):
        value = _int(_field(event, key))
        if value is not None:
            return max(0, value)
    due = _day(_field(event, "due_date"))
    if due is None:
        for entry in entries:
            if _invoice(entry) != invoice_id or _type(entry) not in INVOICE_TYPES:
                continue
            due = _day(_payload(entry).get("due_date"))
            if due is not None:
                break
    if due is not None:
        return max(0, (event.received_at.date() - due).days)
    return 1 if event.type == "invoice.overdue" else 0


def _paid(event: Event, entries: list[LedgerEntry], invoice_id: str) -> bool:
    if event.type == "invoice.paid":
        return True
    explicit = _field(event, "paid")
    if explicit in (True, 1, "1", "true", "True"):
        return True
    if str(_field(event, "status") or "").lower() == "paid":
        return True
    return any(
        _invoice(entry) == invoice_id and _type(entry) in PAYMENT_TYPES and _verified(entry)
        for entry in entries
    )


def _reminders_sent(event: Event, entries: list[LedgerEntry], invoice_id: str) -> int:
    explicit = _int(_field(event, "reminders_sent")) or 0
    aliases = {invoice_id}
    paypal_id = _field(event, "paypal_invoice_id")
    if paypal_id:
        aliases.add(str(paypal_id))
    ledger_count = 0
    for entry in entries:
        if entry.kind != "decision":
            continue
        payload = _payload(entry)
        args = payload.get("args") or {}
        if payload.get("agent") != "collector" or payload.get("tool") != REMINDER_TOOL:
            continue
        if payload.get("outcome") != "allow":
            continue
        if str(args.get("invoice_id") or entry.subject_id) in aliases:
            ledger_count += 1
    return max(explicit, ledger_count)


def _history(event: Event) -> tuple[int, int]:
    raw = event.data.get("client_history") or event.data.get("client") or {}
    if not isinstance(raw, dict):
        raw = {}
    total = _int(raw.get("total_invoices") or raw.get("prior_invoices") or raw.get("invoices")) or 0
    late = _int(raw.get("late_invoices") or raw.get("late_payments") or raw.get("late_count")) or 0
    return max(0, total), max(0, late)


def _average_amount(event: Event, entries: list[LedgerEntry]) -> int | None:
    explicit = _int(_field(event, "average_invoice_cents"))
    if explicit and explicit > 0:
        return explicit
    amounts: dict[str, int] = {}
    for entry in entries:
        if _type(entry) not in INVOICE_TYPES | PAYMENT_TYPES:
            continue
        amount = _int(_payload(entry).get("amount_cents"))
        if amount and amount > 0:
            amounts.setdefault(_invoice(entry), amount)
    if not amounts:
        return None
    return round(sum(amounts.values()) / len(amounts))


def _risk(
    days: int,
    amount: int | None,
    average: int | None,
    total_invoices: int,
    late_invoices: int,
    reminders: int,
    overdue: bool,
    paid: bool,
) -> str:
    if paid or not overdue:
        return "low"
    late_ratio = late_invoices / total_invoices if total_invoices else 0.0
    high_value = bool(amount and average and average > 0 and amount >= average * 2)
    high_history = total_invoices >= 2 and late_ratio >= 0.5
    if days >= 21 or reminders >= 2:
        return "high"
    if days >= 14 and (high_value or high_history or reminders >= 1):
        return "high"
    if days >= 7 or high_value or high_history or reminders >= 1:
        return "med"
    return "low"


def _tone(days: int, risk: str, reminders: int, overdue: bool, paid: bool) -> str:
    if paid or not overdue:
        return "friendly"
    if reminders >= 2 or days >= 30:
        return "final"
    if reminders >= 1 or days >= 14 or risk == "high":
        return "firm"
    return "friendly"


def _next_action(days: int, reminders: int, overdue: bool, paid: bool) -> str:
    if paid or not overdue:
        return "wait"
    if reminders >= 2 or days >= 45:
        return "escalate"
    return "remind"


def _fallback_note(
    invoice_id: str,
    amount: int | None,
    currency: str,
    days: int,
    tone: str,
    action: str,
    paid: bool,
    reminders: int,
) -> str:
    if paid:
        return f"Payment for invoice {invoice_id} is already recorded. No reminder was sent."
    if action == "wait":
        return f"Invoice {invoice_id} is not past due. No reminder was sent."
    if action == "escalate":
        return (
            f"Invoice {invoice_id} for {_money(amount, currency)} is {_days_phrase(days)} past due "
            f"after {reminders} reminder(s). No further reminder was sent; this needs manual review."
        )
    money = _money(amount, currency)
    if tone == "final":
        return (
            f"Hi, invoice {invoice_id} for {money} is now {_days_phrase(days)} past due. "
            "Please pay now or reply with a payment date so we can keep the order open."
        )
    if tone == "firm":
        return (
            f"Hi, invoice {invoice_id} for {money} is now {_days_phrase(days)} past due. "
            "Please arrange payment or reply with an update."
        )
    return (
        f"Hi, a friendly reminder that invoice {invoice_id} for {money} is "
        f"{_days_phrase(days)} past due. Could you let us know when payment will be sent? Thank you."
    )


def _safe_note(note: str, invoice_id: str, amount_cents: int | None) -> bool:
    text = " ".join(str(note or "").split())
    if not 20 <= len(text) <= 500:
        return False
    lowered = text.lower()
    if invoice_id.lower() not in lowered:
        return False
    if amount_cents is not None:
        compact = re.sub(r"[\s,$]", "", text)
        if f"{amount_cents / 100:.2f}" not in compact:
            return False
    return THREAT_RE.search(lowered) is None


def _llm_note(
    event: Event,
    ctx: AgentContext,
    invoice_id: str,
    amount: int | None,
    currency: str,
    days: int,
    reminders: int,
    risk: str,
    tone: str,
    action: str,
    total_invoices: int,
    late_invoices: int,
    fallback: str,
) -> str:
    try:
        prompt = load_prompt("collector")
        payload = json.dumps({
            "event": {"type": event.type, "subject_id": event.subject_id},
            "invoice": {
                "invoice_id": invoice_id,
                "amount_cents": amount,
                "currency": currency,
                "days_overdue": days,
            },
            "client_history": {
                "total_invoices": total_invoices,
                "late_invoices": late_invoices,
            },
            "plan": {
                "reminders_sent": reminders,
                "risk": risk,
                "tone": tone,
                "next_action": action,
            },
        }, sort_keys=True)
        draft = ctx.llm(prompt, f"<untrusted>\n{payload}\n</untrusted>", CollectorPlan)
        candidate = " ".join(str(draft.reminder_note or "").split())
        if _safe_note(candidate, invoice_id, amount):
            return candidate
        ctx.log("note", "collector: LLM note rejected; using deterministic note")
    except LLMError as exc:
        ctx.log("note", f"llm error: {exc}")
    return fallback


def handle(event: Event, ctx: AgentContext) -> CollectorPlan:
    invoice_id = str(_field(event, "invoice_id") or event.subject_id)
    entries = ctx.ledger_find(limit=1000)
    amount = _int(_field(event, "amount_cents"))
    currency = str(_field(event, "currency") or "USD")
    paid = _paid(event, entries, invoice_id)
    days = _days_overdue(event, entries, invoice_id)
    overdue = event.type == "invoice.overdue" and not paid and days > 0
    reminders = _reminders_sent(event, entries, invoice_id)
    total_invoices, late_invoices = _history(event)
    average = _average_amount(event, entries)

    risk = _risk(days, amount, average, total_invoices, late_invoices, reminders, overdue, paid)
    tone = _tone(days, risk, reminders, overdue, paid)
    action = _next_action(days, reminders, overdue, paid)
    note = _fallback_note(invoice_id, amount, currency, days, tone, action, paid, reminders)

    ctx.log(
        "note",
        f"collector: invoice={invoice_id} days={days} reminders={reminders} "
        f"risk={risk} tone={tone} action={action}",
    )

    if action == "remind":
        note = _llm_note(
            event, ctx, invoice_id, amount, currency, days, reminders,
            risk, tone, action, total_invoices, late_invoices, note,
        )
        tool_invoice_id = str(_field(event, "paypal_invoice_id") or invoice_id)
        decision = ctx.tool(
            REMINDER_TOOL,
            {
                "invoice_id": tool_invoice_id,
                "subject": f"Payment reminder for {invoice_id}",
                "note": note,
            },
            f"Collector {tone} reminder for {invoice_id}, {_days_phrase(days)} overdue",
        )
        ctx.log("note", f"collector: reminder outcome={decision.outcome}")

    return CollectorPlan(
        invoice_id=invoice_id,
        risk=risk,
        days_overdue=days,
        tone=tone,
        reminder_note=note,
        next_action=action,
    )
