"""Guardian (P1): keep tracking in sync and compute a cited account-health report."""
from __future__ import annotations

import json
from datetime import date, datetime

from app.agents.base import AgentContext, load_prompt
from app.llm import LLMError
from app.models import Event, HealthFactor, HealthReport, LedgerEntry

PAYMENT_TYPES = {"payment.captured", "invoice.paid"}
REFUND_TYPES = {"payment.refunded"}
SHIPMENT_TYPES = {"shipment.created"}
DELIVERY_TYPES = {"delivery.confirmed"}
EVIDENCE_TYPES = PAYMENT_TYPES | SHIPMENT_TYPES | DELIVERY_TYPES


def _payload(entry: LedgerEntry) -> dict:
    return entry.payload or {}


def _type(entry: LedgerEntry) -> str:
    return str(_payload(entry).get("type", "")).lower()


def _verified(entry: LedgerEntry) -> bool:
    return _payload(entry).get("verified") in (True, 1, "1", "true", "True")


def _invoice(entry: LedgerEntry) -> str:
    return str(_payload(entry).get("invoice_id") or entry.subject_id)


def _event_invoice(event: Event) -> str:
    return str(event.data.get("invoice_id") or event.data.get("subject_id") or event.subject_id)


def _day(value) -> date | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _latest(entries: list[LedgerEntry], types: set[str], invoice_id: str | None = None) -> LedgerEntry | None:
    for entry in entries:
        if _type(entry) in types and (invoice_id is None or _invoice(entry) == invoice_id):
            return entry
    return None


def _payment(entries: list[LedgerEntry], invoice_id: str) -> LedgerEntry | None:
    for entry in entries:
        if _type(entry) in PAYMENT_TYPES and _invoice(entry) == invoice_id and _verified(entry):
            return entry
    return None


def _transaction_id(payment: LedgerEntry | None, event: Event, invoice_id: str) -> str:
    payload = payment.payload if payment else {}
    return str(
        event.data.get("transaction_id")
        or payload.get("transaction_id")
        or payload.get("capture_id")
        or event.data.get("capture_id")
        or invoice_id
    )


def _tracking_context(entries: list[LedgerEntry], event: Event) -> tuple[str, str, str, str] | None:
    invoice_id = _event_invoice(event)
    shipment = _latest(entries, SHIPMENT_TYPES, invoice_id)
    shipment_payload = shipment.payload if shipment else {}
    tracking_number = event.data.get("tracking_number") or shipment_payload.get("tracking_number")
    if not tracking_number:
        return None
    carrier = str(event.data.get("carrier") or shipment_payload.get("carrier") or "OTHER")
    payment = _payment(entries, invoice_id)
    transaction_id = _transaction_id(payment, event, invoice_id)
    return invoice_id, str(tracking_number), carrier, transaction_id


def _sync_tracking(event: Event, ctx: AgentContext, entries: list[LedgerEntry]) -> None:
    if event.type == "shipment.created":
        context = _tracking_context(entries, event)
        if context is None:
            ctx.log("note", "guardian: shipment.created has no tracking number; skipped PayPal sync")
            return
        invoice_id, tracking_number, carrier, transaction_id = context
        ctx.tool(
            "create_shipment_tracking",
            {
                "invoice_id": invoice_id,
                "transaction_id": transaction_id,
                "tracking_number": tracking_number,
                "carrier": carrier,
                "status": str(event.data.get("status") or "SHIPPED"),
            },
            f"register {carrier} tracking for {invoice_id}",
        )
    elif event.type == "delivery.confirmed":
        context = _tracking_context(entries, event)
        if context is None:
            ctx.log("note", "guardian: delivery.confirmed has no shipment tracking; skipped PayPal update")
            return
        invoice_id, tracking_number, carrier, transaction_id = context
        ctx.tool(
            "update_shipment_tracking",
            {
                "invoice_id": invoice_id,
                "transaction_id": transaction_id,
                "tracking_number": tracking_number,
                "carrier": carrier,
                "status": "DELIVERED",
            },
            f"mark {invoice_id} delivered with {carrier} tracking",
        )


def _payments(entries: list[LedgerEntry]) -> dict[str, LedgerEntry]:
    out: dict[str, LedgerEntry] = {}
    for entry in entries:
        if _type(entry) in PAYMENT_TYPES and _verified(entry):
            out.setdefault(_invoice(entry), entry)
    return out


def _sales(entries: list[LedgerEntry], payments: dict[str, LedgerEntry]) -> dict:
    today = date.today()
    last7 = 0
    total30 = 0
    for entry in payments.values():
        payload = _payload(entry)
        amount = payload.get("amount_cents")
        if not isinstance(amount, int) or isinstance(amount, bool):
            continue
        paid_day = _day(payload.get("paid_at")) or entry.created_at.date()
        age = (today - paid_day).days
        if 0 <= age <= 30:
            total30 += amount
        if 0 <= age <= 7:
            last7 += amount
    expected7 = total30 / 30 * 7 if total30 else 0
    enough_history = len(payments) >= 5 and expected7 > 0
    ratio = last7 / expected7 if enough_history else 1.0
    return {"last7_cents": last7, "total30_cents": total30, "ratio": ratio,
            "enough_history": enough_history}


def _metrics(entries: list[LedgerEntry]) -> tuple[dict, dict[str, bool], list[HealthFactor]]:
    payments = _payments(entries)
    paid_count = len(payments)

    refunded = {_invoice(entry) for entry in entries if _type(entry) in REFUND_TYPES} & set(payments)
    refund_rate = min(100.0, len(refunded) / paid_count * 100) if paid_count else 0.0

    created = {entry.subject_id for entry in entries if _type(entry) == "dispute.created"}
    resolved = {entry.subject_id for entry in entries if _type(entry) == "dispute.resolved"}
    open_disputes = len(created - resolved)
    dispute_rate = min(100.0, open_disputes / paid_count * 100) if paid_count else 0.0

    tracked = {_invoice(entry) for entry in entries if _type(entry) in SHIPMENT_TYPES}
    tracking_coverage = len(set(payments) & tracked) / paid_count * 100 if paid_count else 100.0

    sales = _sales(entries, payments)
    ratio = sales["ratio"]
    spike_bad = sales["enough_history"] and ratio > 2.0

    flags = {
        "dispute_rate": open_disputes > 0,
        "refund_rate": refund_rate > 20.0,
        "tracking_coverage": tracking_coverage < 80.0,
        "sales_spike": spike_bad,
    }
    factors = [
        HealthFactor(
            name="open_disputes",
            value=open_disputes,
            impact="negative" if open_disputes else "positive",
            note=f"{open_disputes} open dispute(s); {dispute_rate:.1f}% of paid invoices.",
        ),
        HealthFactor(
            name="refund_rate",
            value=round(refund_rate, 1),
            impact="negative" if refund_rate > 20.0 else "positive",
            note=f"{len(refunded)} refunded invoice(s); {refund_rate:.1f}% refund rate.",
        ),
        HealthFactor(
            name="tracking_coverage",
            value=round(tracking_coverage, 1),
            impact="negative" if tracking_coverage < 80.0 else "positive",
            note=f"{len(set(payments) & tracked)} of {paid_count} paid invoice(s) have tracking.",
        ),
        HealthFactor(
            name="sales_spike",
            value=round(ratio, 2),
            impact="negative" if spike_bad else ("neutral" if not sales["enough_history"] else "positive"),
            note=(
                f"Last 7 days ${sales['last7_cents'] / 100:.2f} vs "
                f"30 days ${sales['total30_cents'] / 100:.2f}."
                if sales["enough_history"]
                else "Not enough payment history to detect a spike."
            ),
        ),
    ]
    metrics = {
        "paid_invoices": paid_count,
        "open_disputes": open_disputes,
        "dispute_rate": round(dispute_rate, 1),
        "refund_rate": round(refund_rate, 1),
        "tracking_coverage": round(tracking_coverage, 1),
        "sales_spike_ratio": round(ratio, 2),
        "sales_spike_enough_history": sales["enough_history"],
        "last7_cents": sales["last7_cents"],
        "total30_cents": sales["total30_cents"],
    }
    return metrics, flags, factors


def _score(metrics: dict, flags: dict) -> int:
    score = 100
    score -= min(45, metrics["open_disputes"] * 15)
    score -= min(20, round(metrics["refund_rate"] * 0.2))
    score -= round((100 - metrics["tracking_coverage"]) * 0.3)
    if flags["sales_spike"]:
        score -= 10
    return max(0, min(100, score))


def _fallback_recommendations(flags: dict) -> list[str]:
    recs = []
    if flags["dispute_rate"]:
        recs.append("Respond to open disputes with the sealed evidence pack.")
    if flags["refund_rate"]:
        recs.append("Review refund causes and tighten fulfillment checks.")
    if flags["tracking_coverage"]:
        recs.append("Add tracking to paid orders before shipping.")
    if flags["sales_spike"]:
        recs.append("Confirm stock and fulfillment capacity for the sales spike.")
    return recs[:3] or ["No urgent issues; keep sealing payment, shipment, and delivery events."]


def _recommendations(
    event: Event,
    ctx: AgentContext,
    metrics: dict,
    factors: list[HealthFactor],
    flags: dict,
) -> list[str]:
    fallback = _fallback_recommendations(flags)
    try:
        prompt = load_prompt("guardian")
        untrusted = json.dumps({
            "event": {"type": event.type, "subject_id": event.subject_id, "data": event.data},
            "metrics": metrics,
            "factors": [factor.model_dump() for factor in factors],
        }, sort_keys=True)
        report = ctx.llm(prompt, f"<untrusted>\n{untrusted}\n</untrusted>", HealthReport)
        recommendations = [str(item).strip() for item in report.recommendations if str(item).strip()]
        if recommendations:
            return recommendations[:3]
    except LLMError as exc:
        ctx.log("note", f"llm error: {exc}")
    return fallback


def _appeal_pack(entries: list[LedgerEntry]) -> str | None:
    created = {
        entry.subject_id: entry for entry in reversed(entries)
        if _type(entry) == "dispute.created"
    }
    resolved = {entry.subject_id for entry in entries if _type(entry) == "dispute.resolved"}
    open_disputes = [(subject_id, entry) for subject_id, entry in created.items() if subject_id not in resolved]
    if not open_disputes:
        return "No open disputes in the sealed ledger."

    lines = ["AegisFleet sealed evidence summary:"]
    for subject_id, dispute in sorted(open_disputes, key=lambda item: item[0]):
        invoice_id = _invoice(dispute)
        related = [
            str(entry.id) for entry in reversed(entries)
            if _type(entry) in EVIDENCE_TYPES and _invoice(entry) == invoice_id
        ][:4]
        evidence = f"ledger #{', #'.join(related)}" if related else "no invoice evidence"
        lines.append(
            f"- Dispute {subject_id} (ledger #{dispute.id}, invoice {invoice_id}): {evidence}."
        )
    return "\n".join(lines)


def handle(event: Event, ctx: AgentContext) -> HealthReport:
    entries = ctx.ledger_find(limit=1000)
    _sync_tracking(event, ctx, entries)

    metrics, flags, factors = _metrics(entries)
    score = _score(metrics, flags)
    recommendations = _recommendations(event, ctx, metrics, factors, flags)
    appeal_pack = _appeal_pack(entries) if event.data.get("request_appeal_pack") else None

    ctx.log(
        "note",
        f"guardian: score={score} open_disputes={metrics['open_disputes']} "
        f"tracking_coverage={metrics['tracking_coverage']:.1f}%",
    )
    return HealthReport(
        score=score,
        factors=factors,
        recommendations=recommendations,
        appeal_pack=appeal_pack,
    )
