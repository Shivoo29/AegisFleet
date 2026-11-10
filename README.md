# AegisFleet

**Stop losing money to fake payments, held funds, and friendly-fraud disputes.**
AegisFleet runs 4 AI agents (Sentinel, Defender, Collector, Guardian) behind a
guardrail gateway. AI may draft, classify, and recommend — only rules or a
human move money.

## The four agents

| Agent | Trigger | Job | Hard boundary |
|---|---|---|---|
| **Sentinel** | Suspicious “payment received” email | Verifies the sender domain and amount against sealed ledger payments; flags lookalikes, urgency, off-platform asks, overpayment, and prompt injection. | Read-only. It never calls a tool or moves money. |
| **Defender** | Dispute opened | Gathers sealed payment, tracking, and delivery records; classifies the claim; drafts evidence and recommends provide evidence, refund, or accept. | Every fact cites a ledger entry. Refunds and offers are held for human approval. |
| **Collector** | `invoice.overdue` event | Scores risk deterministically, chooses tone and action, counts prior reminders from the ledger, and drafts a capped reminder. | No new amount, discount, waiver, or payment call. |
| **Guardian** | Payment, shipment, or delivery event | Registers tracking, marks delivery, scores account health from ledger facts, and drafts appeal notes. | Health score is rule-based. Every appeal line cites a ledger entry, and PayPal writes stay behind the gateway. |

## Safety invariants

- Agents receive an `AgentContext`, not a database or PayPal client: they can only use `ctx.tool()`, `ctx.llm()`, and `ctx.ledger_find()`.
- The gateway checks the kill switch, per-agent allowlist, argument schema, and weekly caps. Anything that moves money is held until a human approves it.
- LLM output is validated against Pydantic schemas, retried once on invalid JSON, then replaced by deterministic rules.
- Email and dispute text is untrusted data. It is fenced in prompts, never followed as instructions, and injection attempts are flagged before they can steer a tool call.

## First run

```bash
# 1. Start Postgres
docker compose up -d db

# 2. Backend
cd backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload

# 3. Frontend
cd ../frontend
npm install && npm run build
```

Then open http://localhost:8000 (API serves the built frontend) or
http://localhost:5173 (Vite dev server, proxies `/api` and `/webhooks`).

## Env

Copy `.env.example` → `.env`. `PAYPAL_MODE=fake` and `LLM_PROVIDER=fake` are
the defaults; `PAYPAL_MODE=live` refuses to start.

## Evals

Labelled suites run against the real model, or fully offline with `LLM_PROVIDER=fake`:

```bash
cd backend
python -m evals.run --agent sentinel --reset
python -m evals.run --agent defender --reset
python -m evals.run --agent collector --reset
python -m evals.run --agent injection --reset
```

| Suite | n | Latest real-model result |
|---|---:|---|
| Sentinel | 20 | 20/20, 0 scams missed, 0 false alarms |
| Defender | 8 | 8/8 action, 8/8 classification, 0 uncited facts |
| Collector | 10 | 10/10 action, 10/10 classification |
| Injection | 6 | 6/6 scam, 6/6 flagged, 0 tool calls, 6/6 disallowed tools denied |

The injection suite also re-checks the gateway, so a fixture only passes when every tool it tries to invoke is denied.

## AI tools used

| Tool | Model | How we use it |
|---|---|---|
| Groq | `openai/gpt-oss-120b` | Primary model for Sentinel, Defender, Collector, and Guardian. Structured JSON is validated against Pydantic schemas. |
| Google Gemini API | `gemini-3.5-flash` | First fallback when Groq is rate-limited or errors. |
| NVIDIA NIM | `nemotron-3.5-super-vl-120b-a12b` | Second fallback. |
| AG Grid Community | – | Proof Ledger table, filtering, and highlighting the broken row after tampering. |

The models never call PayPal and never hold credentials. They return structured recommendations; deterministic rules and the gateway decide what runs.
