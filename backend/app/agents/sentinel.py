"""Sentinel (P0): classify payment emails with deterministic guards."""
from __future__ import annotations

import re
from urllib.parse import urlsplit

from app.agents.base import AgentContext, load_prompt
from app.llm import LLMError
from app.models import Event, LedgerEntry, SentinelVerdict

TRUSTED_DOMAINS = ("paypal.com",)
PAYMENT_EVENT_TYPES = ("payment.captured", "invoice.paid")
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly"}

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
INVOICE_RE = re.compile(r"\b(?:INV|TXN|PP[-_]?D)[-_ ]?[A-Z0-9]{2,}\b", re.IGNORECASE)
AMOUNT_RE = re.compile(
    r"(?<![A-Z0-9])\$\s?([0-9][0-9,]*(?:\.[0-9]{2})?)"
    r"|(?<![A-Z0-9])([0-9][0-9,]*(?:\.[0-9]{2})?)\s?(?:USD|usd)\b"
)
PAYMENT_CLAIM_RE = re.compile(
    r"\b(?:payment|funds|invoice)\b.{0,40}\b(?:received|sent|paid|confirmed|completed|"
    r"on hold|available|pending|cleared|released)\b",
    re.IGNORECASE | re.DOTALL,
)
INJECTION_PATTERNS = (
    r"\b(?:ignore|disregard|forget)\b.{0,60}\b(?:previous|prior|above|system|developer)\b"
    r".{0,30}\b(?:instructions?|prompts?|rules?|ledger)\b",
    r"\b(?:system|developer|assistant)\s*(?:message|prompt|instruction)?\s*:",
    r"\b(?:call|invoke|run|execute|use)\b.{0,40}\b(?:tool|function)\b",
    r"\b(?:call|invoke|run|execute|use)\b.{0,60}\b(?:create_refund|send_invoice_reminder|"
    r"provide_dispute_evidence|accept_dispute_claim|make_dispute_offer|create_shipment_tracking|"
    r"update_shipment_tracking)\b",
    r"\bmark\b.{0,40}\b(?:this|the email|it)\b.{0,30}\b(?:legit|safe|paid|verified)\b",
    r"\b(?:override|bypass)\b.{0,35}\b(?:ledger|gateway|rules?|verdict)\b",
    r"\b(?:tool_call|function_call)\b",
    r"\{\s*[\"']?(?:tool|function|tool_call)[\"']?\s*:",
)
INJECTION_RE = re.compile(
    "|".join(f"(?:{pattern})" for pattern in INJECTION_PATTERNS),
    re.IGNORECASE | re.DOTALL,
)

CREDENTIAL_PHRASES = (
    "verify your account",
    "verify your identity",
    "confirm your identity",
    "confirm your account",
    "confirm your payout",
    "update your payment information",
    "log in to confirm",
    "sign in to verify",
    "enter your password",
    "one-time code",
    "security code",
    "otp",
)
URGENCY_PHRASES = (
    "urgent",
    "immediately",
    "act now",
    "within 24 hours",
    "within 12 hours",
    "final notice",
    "final warning",
    "account has been limited",
    "account will be limited",
    "account will be suspended",
    "account has been suspended",
)
OFF_PLATFORM_PHRASES = (
    "gift card",
    "gift cards",
    "western union",
    "moneygram",
    "wire transfer",
    "zelle",
    "venmo",
    "cash app",
    "bitcoin",
    "crypto",
    "usdt",
    "ethereum",
)
OVERPAYMENT_PHRASES = (
    "overpaid",
    "overpayment",
    "refund the difference",
    "send back the extra",
    "extra amount",
)
UPFRONT_SHIP_PHRASES = (
    "funds are on hold until you ship",
    "payment is on hold until you ship",
    "until you ship",
    "once you ship",
    "ship first",
    "ship immediately",
    "send tracking before",
    "send tracking to release",
    "release the funds",
)


def _translate(text: str) -> str:
    return text.translate(str.maketrans({"1": "l", "0": "o", "3": "e", "4": "a", "5": "s", "7": "t"}))


def _sender_domain(sender: str) -> str:
    match = EMAIL_RE.search(sender or "")
    return match.group(1).lower().strip(".") if match else ""


def _is_trusted(domain: str) -> bool:
    return any(domain == d or domain.endswith(f".{d}") for d in TRUSTED_DOMAINS)


def _looks_like_brand(value: str) -> bool:
    return "paypal" in _translate(value.lower())


def _suspicious_domain(domain: str) -> bool:
    return bool(domain) and not _is_trusted(domain) and _looks_like_brand(domain)


def _host(url: str) -> str:
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def _suspicious_urls(text: str) -> list[str]:
    found = []
    for url in URL_RE.findall(text):
        host = _host(url)
        if not host or _is_trusted(host):
            continue
        if host in SHORTENERS or _looks_like_brand(host) or re.fullmatch(r"\d+(?:\.\d+){3}", host):
            found.append(url)
    return found


def _amounts_cents(text: str) -> list[int]:
    values = []
    for match in AMOUNT_RE.finditer(text):
        raw = match.group(1) or match.group(2)
        if raw:
            cents = int(round(float(raw.replace(",", "")) * 100))
            if cents not in values:
                values.append(cents)
    return values


def _invoice_id(event: Event, text: str) -> str | None:
    subject = str(event.subject_id or "").strip()
    if re.match(r"^(?:INV|TXN|PP[-_]?D)", subject, re.IGNORECASE):
        return subject.upper()
    match = INVOICE_RE.search(text)
    if match:
        return re.sub(r"[-_ ]", "-", match.group(0)).upper()
    return subject or None


def _verified_payments(ctx: AgentContext, invoice_id: str | None) -> list[LedgerEntry]:
    if not invoice_id:
        return []
    entries = ctx.ledger_find(kind="event", subject_id=invoice_id, limit=200)
    matches = []
    for entry in entries:
        payload = entry.payload or {}
        kind = str(payload.get("type", "")).lower()
        verified = payload.get("verified")
        if kind in PAYMENT_EVENT_TYPES and verified in (True, 1, "1", "true", "True"):
            matches.append(entry)
    return matches


def _detect_signals(text: str, sender_domain: str, urls: list[str]) -> list[str]:
    lowered = text.lower()
    flags: list[str] = []

    if _suspicious_domain(sender_domain):
        flags.append("lookalike sender domain")
    if urls:
        flags.append("link does not resolve to paypal.com")
    for phrase in CREDENTIAL_PHRASES:
        if phrase in lowered:
            flags.append("asks for account verification or credentials")
            break
    for phrase in URGENCY_PHRASES:
        if phrase in lowered:
            flags.append("creates false urgency")
            break
    for phrase in OFF_PLATFORM_PHRASES:
        if phrase in lowered:
            flags.append("requests off-platform payment")
            break
    for phrase in OVERPAYMENT_PHRASES:
        if phrase in lowered:
            flags.append("overpayment or refund-the-difference pattern")
            break
    for phrase in UPFRONT_SHIP_PHRASES:
        if phrase in lowered:
            flags.append("asks to ship before funds clear")
            break
    if INJECTION_RE.search(text):
        flags.append("contains instructions aimed at the AI")
    return flags


def _pick_match(matches: list[LedgerEntry], amounts: list[int]) -> LedgerEntry | None:
    if not matches:
        return None
    if amounts:
        for entry in matches:
            amount = (entry.payload or {}).get("amount_cents")
            if amount is not None and int(amount) in amounts:
                return entry
        for entry in matches:
            if (entry.payload or {}).get("amount_cents") is None:
                return entry
    return matches[0]


def _amount_mismatch(matches: list[LedgerEntry], amounts: list[int]) -> bool:
    if not matches or not amounts:
        return False
    known_amounts = {
        int(entry.payload["amount_cents"])
        for entry in matches
        if (entry.payload or {}).get("amount_cents") is not None
    }
    if not known_amounts:
        return False
    return not any(amount in known_amounts for amount in amounts)


def _explain_scam(
    invoice_id: str | None,
    signals: list[str],
    claims_payment: bool,
    matches: list[LedgerEntry],
    mismatch: bool,
) -> str:
    parts: list[str] = []
    if claims_payment and not matches:
        parts.append(f"We found no verified PayPal payment for {invoice_id or 'this invoice'}.")
    elif mismatch:
        parts.append("The verified PayPal amount does not match the email.")
    if "lookalike sender domain" in signals:
        parts.append("The sender is not paypal.com.")
    elif "link does not resolve to paypal.com" in signals:
        parts.append("The link does not go to paypal.com.")
    elif "asks for account verification or credentials" in signals:
        parts.append("It asks for account details or a login code.")
    elif "requests off-platform payment" in signals:
        parts.append("It asks for an unsafe payment method.")
    elif "overpayment or refund-the-difference pattern" in signals:
        parts.append("It asks you to send money back.")
    elif "contains instructions aimed at the AI" in signals:
        parts.append("It contains instructions aimed at the AI, not at a person.")
    elif "creates false urgency" in signals:
        parts.append("It pressures you to act quickly.")
    elif "asks to ship before funds clear" in signals:
        parts.append("It asks you to ship before the money is secure.")
    if not parts:
        parts.append("The email does not match the ledger.")
    parts.append("Don't ship yet.")
    return " ".join(parts[:3])


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def handle(event: Event, ctx: AgentContext) -> SentinelVerdict:
    body = str(event.data.get("body", ""))
    subject = str(event.data.get("subject", ""))
    sender = str(event.data.get("from") or event.data.get("sender") or "")
    text = f"{subject}\n{body}"

    sender_domain = _sender_domain(sender)
    urls = _suspicious_urls(text)
    invoice_id = _invoice_id(event, text)
    amounts = _amounts_cents(text)
    claims_payment = bool(PAYMENT_CLAIM_RE.search(text))
    matches = _verified_payments(ctx, invoice_id)
    matched = _pick_match(matches, amounts)
    mismatch = _amount_mismatch(matches, amounts)

    ctx.log("note", f"sentinel: invoice={invoice_id} sender_domain={sender_domain or '-'} matches={len(matches)}")

    signals = _detect_signals(text, sender_domain, urls)
    hard_scam = bool(signals)
    if claims_payment and not matches:
        hard_scam = True
        signals.append("claims payment not present in ledger")
    if mismatch:
        hard_scam = True
        signals.append("amount does not match the verified payment")

    llm_verdict = SentinelVerdict(verdict="unsure", confidence=0.0)
    try:
        prompt = load_prompt("sentinel")
        wrapped = f"<untrusted>\nFrom: {sender}\nSubject: {subject}\n\n{body}\n</untrusted>"
        llm_verdict = ctx.llm(prompt, wrapped, SentinelVerdict)
    except LLMError as exc:
        ctx.log("note", f"llm error: {exc}")

    llm_flags = llm_verdict.red_flags if llm_verdict.verdict != "legit" else []
    red_flags = _dedupe(signals + list(llm_flags))

    matched_id = matched.id if matched else None

    if hard_scam:
        verdict = "scam"
        confidence = max(0.9, llm_verdict.confidence if llm_verdict.verdict == "scam" else 0.0)
        explanation = _explain_scam(invoice_id, signals, claims_payment, matches, mismatch)
    elif matched is not None:
        if llm_verdict.verdict == "scam" and llm_verdict.red_flags:
            verdict = "scam"
            confidence = max(0.75, llm_verdict.confidence)
            explanation = (
                "A PayPal payment is verified, but the email has suspicious details. "
                "Check it in PayPal before acting."
            )
        else:
            verdict = "legit"
            confidence = 0.95
            explanation = (
                f"We found verified PayPal payment #{matched.id} for {invoice_id}. "
                "The funds are confirmed."
            )
    elif llm_verdict.verdict == "scam":
        verdict = "scam"
        confidence = max(0.7, llm_verdict.confidence)
        explanation = "The email looks like a scam. Check the payment in PayPal before shipping."
    else:
        verdict = "unsure"
        confidence = 0.35
        explanation = (
            "We could not confirm a verified PayPal payment. "
            "Check your PayPal account before shipping."
        )

    if claims_payment and "claims payment not present in ledger" in signals:
        confidence = max(confidence, 0.9)

    return SentinelVerdict(
        verdict=verdict,
        confidence=round(min(max(confidence, 0.0), 1.0), 2),
        matched_payment_entry_id=matched_id,
        red_flags=red_flags,
        explanation=explanation,
    )
