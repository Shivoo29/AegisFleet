"""Defender (P0): build a cited evidence pack and recommend one dispute action."""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta, timezone

from app.agents.base import AgentContext, load_prompt
from app.llm import LLMError
from app.models import EvidencePack, Event, Fact, LedgerEntry

INR = "MERCHANDISE_OR_SERVICE_NOT_RECEIVED"
SNAD = "MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED"
UNAUTHORIZED = "UNAUTHORIZED"
DUPLICATE = "DUPLICATE_TRANSACTION"
PAYMENT_TYPES = {"payment.captured", "invoice.paid"}
RECEIVED_PHRASES = ("arrived", "received", "got it", "thanks", "as described")


def _payload(entry: LedgerEntry) -> dict:
    return entry.payload or {}


def _type(entry: LedgerEntry) -> str:
    return str(_payload(entry).get("type", "")).lower()


def _day(value) -> date | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _money(amount_cents: int | None, currency: str) -> str:
    if amount_cents is None:
        return f"the disputed amount ({currency})"
    return f"${amount_cents / 100:.2f} {currency}"


def _dispute(event: Event, tool_result: dict | None) -> dict:
    merged = dict(tool_result or {})
    embedded = event.data.get("dispute") or event.data.get("resource") or {}
    if isinstance(embedded, dict):
        merged.update(embedded)
    return merged


def _amount_cents(event: Event, dispute: dict) -> int | None:
    value = event.data.get("amount_cents")
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    for key in ("amount", "dispute_amount"):
        amount = dispute.get(key)
        if isinstance(amount, dict) and amount.get("value") is not None:
            try:
                return int(round(float(str(amount["value"]).replace(",", "")) * 100))
            except (TypeError, ValueError):
                return None
    return None


def _currency(event: Event, dispute: dict) -> str:
    if event.data.get("currency"):
        return str(event.data["currency"])
    for key in ("amount", "dispute_amount"):
        amount = dispute.get(key)
        if isinstance(amount, dict) and amount.get("currency_code"):
            return str(amount["currency_code"])
    return "USD"


def _invoice_id(event: Event, dispute: dict) -> str | None:
    for value in (event.data.get("invoice_id"), dispute.get("invoice_id")):
        if value:
            return str(value)
    transactions = dispute.get("seller_transactions") or dispute.get("disputed_transactions") or []
    for transaction in transactions:
        if isinstance(transaction, dict):
            value = transaction.get("invoice_id") or transaction.get("invoice_number")
            if value:
                return str(value)
    return None


def _entries(ctx: AgentContext, invoice_id: str | None) -> list[LedgerEntry]:
    if not invoice_id:
        return []
    return ctx.ledger_find(subject_id=invoice_id, limit=300)


def _pick(entries: list[LedgerEntry], types: set[str]) -> list[LedgerEntry]:
    return [entry for entry in entries if _type(entry) in types]


def _verified_payments(entries: list[LedgerEntry]) -> list[LedgerEntry]:
    return [
        entry for entry in _pick(entries, PAYMENT_TYPES)
        if _payload(entry).get("verified") in (True, 1, "1", "true", "True")
    ]


def _payment(payments: list[LedgerEntry], amount_cents: int | None) -> LedgerEntry | None:
    if not payments:
        return None
    if amount_cents is not None:
        for entry in payments:
            recorded = _payload(entry).get("amount_cents")
            if recorded is not None and int(recorded) == amount_cents:
                return entry
    return payments[0]


def _explicit_address_match(*entries: LedgerEntry | None) -> bool | None:
    for entry in entries:
        if entry is None:
            continue
        value = _payload(entry).get("address_match")
        if isinstance(value, bool):
            return value
    return None


def _shipped_in_seven_days(payment: LedgerEntry | None, shipment: LedgerEntry | None) -> bool:
    if payment is None or shipment is None:
        return False
    paid_at = _payload(payment).get("paid_at")
    paid_day = _day(paid_at) or payment.created_at.date()
    shipped_day = _day(_payload(shipment).get("shipped_at"))
    if shipped_day is None:
        return False
    return 0 <= (shipped_day - paid_day).days <= 7


def _checklist(
    shipment: LedgerEntry | None,
    delivery: LedgerEntry | None,
    address_match: bool | None,
    payment: LedgerEntry | None,
) -> dict[str, bool]:
    shipment_payload = _payload(shipment) if shipment else {}
    tracking = shipment_payload.get("tracking_number")
    carrier = shipment_payload.get("carrier")
    return {
        "tracking_online": bool(tracking and carrier),
        "delivered": delivery is not None,
        "address_match": bool(address_match),
        "shipped_in_7_days": _shipped_in_seven_days(payment, shipment),
    }


def _buyer_messages(entries: list[LedgerEntry]) -> list[tuple[LedgerEntry, str]]:
    messages = []
    for entry in entries:
        if _type(entry) != "buyer.message":
            continue
        text = str(_payload(entry).get("message", "")).strip()
        if text:
            messages.append((entry, text))
    return messages


def _buyer_received(messages: list[tuple[LedgerEntry, str]]) -> bool:
    return any(phrase in text.lower() for _, text in messages for phrase in RECEIVED_PHRASES)


def _classify(reason: str, checklist: dict[str, bool], buyer_received: bool) -> tuple[str, float]:
    all_clear = all(checklist.values()) and bool(checklist)
    if all_clear and reason in (INR, UNAUTHORIZED) and buyer_received:
        return "friendly_fraud", 0.9
    if all_clear and reason == INR:
        return "friendly_fraud", 0.85
    if all_clear and reason == SNAD:
        return "genuine", 0.8
    if not all_clear:
        return "genuine", 0.8
    return "unclear", 0.5


def _recommend(classification: str, reason: str, checklist: dict[str, bool]) -> str:
    all_clear = all(checklist.values()) and bool(checklist)
    if all_clear and (reason == INR or classification == "friendly_fraud"):
        return "provide_evidence"
    if not all_clear and reason == DUPLICATE:
        return "accept_claim"
    return "offer_refund"


def _facts(
    payment: LedgerEntry | None,
    shipment: LedgerEntry | None,
    delivery: LedgerEntry | None,
    address_match: bool | None,
    messages: list[tuple[LedgerEntry, str]],
    invoice_id: str | None,
    amount_cents: int | None,
    currency: str,
) -> list[Fact]:
    facts: list[Fact] = []
    if payment is not None:
        facts.append(Fact(
            claim=f"Verified payment of {_money(amount_cents, currency)} was captured for {invoice_id}.",
            ledger_entry_id=payment.id,
        ))
    if shipment is not None:
        payload = _payload(shipment)
        tracking = payload.get("tracking_number", "unknown tracking")
        carrier = payload.get("carrier", "unknown carrier")
        shipped_at = payload.get("shipped_at", "an unknown date")
        facts.append(Fact(
            claim=f"Shipment was created with {carrier} tracking {tracking} on {shipped_at}.",
            ledger_entry_id=shipment.id,
        ))
        if address_match is not None:
            claim = ("The delivery address matches the buyer's address on file."
                     if address_match else "The delivery address does not match the buyer's address on file.")
            facts.append(Fact(claim=claim, ledger_entry_id=shipment.id))
    if delivery is not None:
        payload = _payload(delivery)
        delivered_at = payload.get("delivered_at", "an unknown date")
        delivered_to = payload.get("delivered_to")
        suffix = f" to {delivered_to}" if delivered_to else ""
        facts.append(Fact(
            claim=f"The carrier confirmed delivery on {delivered_at}{suffix}.",
            ledger_entry_id=delivery.id,
        ))
    for entry, text in messages[:2]:
        short = text if len(text) <= 180 else f"{text[:177]}..."
        facts.append(Fact(claim=f"Buyer message: {short}", ledger_entry_id=entry.id))
    return facts


def _note(
    dispute_id: str,
    reason: str,
    checklist: dict[str, bool],
    facts: list[Fact],
    amount_cents: int | None,
    currency: str,
) -> str:
    parts = [f"Dispute {dispute_id} ({reason}) for {_money(amount_cents, currency)}."]
    for fact in facts[:5]:
        parts.append(f"{fact.claim} (ledger #{fact.ledger_entry_id})")
    checklist_text = ", ".join(f"{name}={'yes' if value else 'no'}" for name, value in checklist.items())
    parts.append(f"Evidence checklist: {checklist_text}.")
    return " ".join(parts)


CITE = re.compile(r"#(\d+)")


def _grounded(text: str, facts: list[Fact]) -> tuple[str | None, str]:
    """Accept the model's note only if every ledger id it cites is one of our facts, it cites at least one,
    and it carries no links or addresses. Otherwise the rule-built note is used. Returns (note or None, why)."""
    text = (text or "").strip()
    allowed = {f.ledger_entry_id for f in facts}
    cited = {int(x) for x in CITE.findall(text)}
    if not text or len(text) > 1500:
        return None, "empty or too long"
    if not cited:
        return None, "cites no ledger entries"
    if not cited <= allowed:
        return None, f"cites entries that are not evidence: {sorted(cited - allowed)}"
    if re.search(r"https?://|www\.|@", text):
        return None, "contains a link or address"
    return text, f"{len(cited)} ledger citations, all verified"


def _action_args(action: str, dispute_id: str, note: str, amount_cents: int | None, currency: str) -> tuple[str, dict]:
    if action == "provide_evidence":
        return "provide_dispute_evidence", {
            "dispute_id": dispute_id,
            "evidence_type": "OTHER",
            "note": note,
        }
    if action == "accept_claim":
        return "accept_dispute_claim", {"dispute_id": dispute_id, "note": note}
    return "make_dispute_offer", {
        "dispute_id": dispute_id,
        "amount_cents": amount_cents,
        "disputed_amount_cents": amount_cents,
        "currency": currency,
        "note": note,
    }


def _plan_deadline_guard(ctx: AgentContext, dispute: dict, dispute_id: str) -> None:
    """Defender books its own re-check 48 hours before PayPal's response deadline."""
    try:
        due = datetime.fromisoformat(str(dispute.get("seller_response_due_date") or ""))
    except ValueError:
        return
    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)
    when = due - timedelta(days=2)
    if when > datetime.now(timezone.utc):
        ctx.plan("get_dispute", {"dispute_id": dispute_id, "subject_id": dispute_id},
                 f"re-check {dispute_id} before PayPal's deadline",
                 "Deadline guard: re-check 48h before PayPal decides", when)


def handle(event: Event, ctx: AgentContext) -> EvidencePack:
    dispute_id = str(event.subject_id or "")
    loaded = ctx.act("get_dispute", {"dispute_id": dispute_id}, "load dispute details")
    tool_result = loaded.result if loaded.outcome == "allow" and isinstance(loaded.result, dict) else {}
    dispute = _dispute(event, tool_result)
    dispute_id = str(dispute.get("dispute_id") or dispute_id)
    reason = str(dispute.get("reason") or event.data.get("reason") or "UNKNOWN").upper()
    amount_cents = _amount_cents(event, dispute)
    currency = _currency(event, dispute)
    invoice_id = _invoice_id(event, dispute)

    entries = _entries(ctx, invoice_id)
    payment = _payment(_verified_payments(entries), amount_cents)
    shipment = next(iter(_pick(entries, {"shipment.created"})), None)
    delivery = next(iter(_pick(entries, {"delivery.confirmed"})), None)
    address_match = _explicit_address_match(shipment, delivery)
    checklist = _checklist(shipment, delivery, address_match, payment)
    messages = _buyer_messages(entries)
    buyer_received = _buyer_received(messages)

    ctx.log(
        "note",
        f"defender: dispute={dispute_id} invoice={invoice_id or '-'} reason={reason} "
        f"ledger_entries={len(entries)}",
    )

    facts = _facts(payment, shipment, delivery, address_match, messages, invoice_id, amount_cents, currency)
    classification, confidence = _classify(reason, checklist, buyer_received)
    llm_pack = None
    try:
        prompt = load_prompt("defender")
        untrusted = json.dumps({
            "dispute": dispute,
            "checklist": checklist,
            "facts": [fact.model_dump() for fact in facts],
        }, sort_keys=True)
        llm_pack = ctx.llm(prompt, f"<untrusted>\n{untrusted}\n</untrusted>", EvidencePack)
        if classification == "unclear" and llm_pack.classification != "unclear":
            classification = llm_pack.classification
            confidence = max(0.4, llm_pack.confidence)
    except LLMError as exc:
        ctx.log("note", f"llm error: {exc}")
    action = _recommend(classification, reason, checklist)
    if action == "offer_refund" and not amount_cents:
        action = "accept_claim"
    note = _note(dispute_id, reason, checklist, facts, amount_cents, currency)
    if llm_pack is not None:
        written, why = _grounded(llm_pack.note_to_paypal, facts)
        if written:
            note = f"{written} Evidence checklist: " + ", ".join(
                f"{k}={'yes' if v else 'no'}" for k, v in checklist.items()) + "."
        ctx.log("note", f"defender: AI-written note {'accepted' if written else 'rejected'} ({why})")
    tool, args = _action_args(action, dispute_id, note, amount_cents, currency)
    decision = ctx.act(tool, args, f"Defender recommends {action} for {dispute_id}")
    ctx.log("note", f"defender: action={action} tool={tool} outcome={decision.outcome}")
    _plan_deadline_guard(ctx, dispute, dispute_id)

    return EvidencePack(
        dispute_id=dispute_id,
        reason=reason,
        classification=classification,
        confidence=round(min(max(confidence, 0.0), 1.0), 2),
        checklist=checklist,
        facts=facts,
        note_to_paypal=note,
        recommended_action=action,
    )
