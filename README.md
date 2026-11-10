# AegisFleet

**The brakes for agentic commerce.** AegisFleet is a guardrail gateway between AI
agents and a seller's PayPal account. Its own four agents (Sentinel, Defender,
Collector, Guardian) and any outside agent connected over MCP go through the same
gateway: kill switch, allowlist, caps, human approval for refunds of $100 or more,
and a hash-chained Proof Ledger. AI may draft, classify, recommend and plan; only
rules or a human move money.

Live: https://aegisfleet.solvor.co.in · MCP: `https://aegisfleet.solvor.co.in/mcp` · API docs: https://aegisfleet.solvor.co.in/docs

## Connect an outside agent (MCP)

```bash
claude mcp add --transport http aegisfleet https://aegisfleet.solvor.co.in/mcp \
  --header "Authorization: Basic $(printf 'judge:<password>' | base64)"
```

Eight tools: `create_invoice`, `send_payment_reminder`, `refund_payment`, `check_approval`,
`check_payment_email`, `list_invoices`, `get_history`, `verify_ledger`. Outside agents act as the
gateway identity `external` ([`backend/app/mcp_server.py`](backend/app/mcp_server.py)): they can bill and
refund but never touch disputes, reminders are capped at 2 per invoice per week, and a refund only goes
back to the buyer who paid, for no more than the verified PayPal payment minus refunds already made or
waiting for approval ([`refundable_cents`](backend/app/gateway/rules.py)).

## Agents plan ahead

Agents schedule their own next steps ([`backend/app/plans.py`](backend/app/plans.py)): Collector books a
firmer follow-up and a final notice, Guardian books a carrier check, Defender books a re-check 48 hours
before PayPal's dispute deadline. New facts re-plan (paid cancels the reminders). The seller drags plans on
the Bryntum timeline; a runner sends each due plan through `gateway.call`, so a plan that breaks a rule is
shown blocked with the gateway's reason. Every plan, move, cancel and result is sealed.

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

Latest real-model run (Groq → Gemini → NVIDIA), with its notes: [`docs/evals/2026-11-10-groq.md`](docs/evals/2026-11-10-groq.md).

| Suite | n | Latest real-model result |
|---|---:|---|
| Sentinel | 20 | 20/20, 0 scams missed, 0 false alarms |
| Defender | 8 | 8/8 action, 8/8 classification, 0 uncited facts, 8/8 AI-written notes passed the citation check |
| Collector | 10 | 10/10 risk, 10/10 tone, 10/10 action |
| Injection | 6 | 6/6 scam, 6/6 flagged, 0 tool calls, 6/6 disallowed tools denied |

The injection suite also re-checks the gateway, so a fixture only passes when every tool it tries to invoke is denied.

## API, docs portal and SDKs

- OpenAPI spec: [`docs/api/openapi.json`](docs/api/openapi.json), also live at `/openapi.json`. Regenerate with `cd backend && python ../scripts/export_openapi.py`; a test fails if it drifts.
- Docs portal: https://aegisfleet.solvor.co.in/docs, built by [APIMatic](https://www.apimatic.io) from `apimatic/src` into `apimatic/portal`.
- SDKs: [`apimatic/sdk/python`](apimatic/sdk/python) and [`apimatic/sdk/typescript`](apimatic/sdk/typescript).
- Rebuild after an API change: copy the spec to `apimatic/src/spec/openapi.json`, then in `apimatic/` run `apimatic portal generate -f` and `apimatic sdk generate -l python -f` (and `-l typescript`).
- Swagger UI moved to `/swagger`.

## AI tools used

| Tool | Model | How we use it |
|---|---|---|
| Groq | `openai/gpt-oss-120b` | Primary model for Sentinel, Defender, Collector, and Guardian. Structured JSON is validated against Pydantic schemas. |
| Google Gemini API | `gemini-3.5-flash` | First fallback when Groq is rate-limited or errors. |
| NVIDIA NIM | `nemotron-3.5-super-vl-120b-a12b` | Second fallback. |
| AG Grid Community | – | Proof Ledger table, filtering, and highlighting the broken row after tampering. |

The models never call PayPal and never hold credentials. They return structured recommendations; deterministic rules and the gateway decide what runs.
