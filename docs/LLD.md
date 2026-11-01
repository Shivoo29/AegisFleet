# AegisFleet — Low-Level Design

Frozen contracts. Change only via PR approved by SKJ. Teammate detail: [team/A_agents.md](team/A_agents.md), [team/B_console.md](team/B_console.md).

## 1. Repo layout

```
aegisfleet/
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py          FastAPI app, /healthz, mounts api + webhooks, serves frontend/dist
│   │   ├── config.py        Settings (pydantic-settings); refuses PAYPAL_MODE=live
│   │   ├── models.py        ALL shared Pydantic contracts (Event, Decision, LedgerEntry, agent outputs)
│   │   ├── db.py            psycopg pool, conn() ctx manager, init_schema()
│   │   ├── schema.sql
│   │   ├── ledger.py        seal / verify / find
│   │   ├── events.py        store_event(), route(event) -> runs agent in background
│   │   ├── llm.py           complete(system, user, schema)
│   │   ├── api.py           /api/* router
│   │   ├── demo.py          /api/demo/* (DEMO_MODE only)
│   │   ├── gateway/rules.py, gateway/gateway.py
│   │   ├── paypal/client.py, paypal/fake.py, paypal/webhooks.py
│   │   └── agents/
│   │       ├── base.py       AgentContext            (A owns impl, interface frozen)
│   │       ├── run.py        CLI runner              (A)
│   │       ├── sentinel.py, defender.py, collector.py, guardian.py  (A)
│   │       └── prompts/<agent>.md                    (A writes, SKJ approves)
│   ├── tests/
│   └── evals/run.py, evals/datasets/                 (A)
├── frontend/                                         (B)
├── fixtures/paypal/ (SKJ)  emails/ disputes/ invoices/ (A)
├── scripts/seed_demo.py, reset_demo.py, replay.py
├── docker-compose.yml       Postgres 16 only
├── Dockerfile, render.yaml, .env.example, LICENSE, README.md
└── .github/CODEOWNERS, workflows/ci.yml, pull_request_template.md
```

## 2. Shared models (`app/models.py`)

```py
EventType = Literal["invoice.sent","invoice.overdue","invoice.paid","payment.captured",
  "payment.refunded","email.received","shipment.created","delivery.confirmed",
  "dispute.created","dispute.updated","dispute.resolved"]

class Event(BaseModel):
    id: str; type: EventType
    source: Literal["paypal","inbox","courier","scheduler","console"]
    subject_id: str; data: dict; verified: bool; received_at: datetime

class Decision(BaseModel):
    outcome: Literal["allow","hold","deny"]; reason: str
    approval_id: str | None = None; result: dict | None = None; ledger_entry_id: int

class LedgerEntry(BaseModel):
    id: int; kind: Literal["event","decision","agent_step","approval","note"]
    subject_id: str; summary: str; payload: dict; prev_hash: str; hash: str; created_at: datetime

# Agent outputs: SentinelVerdict, Fact, EvidencePack, CollectorPlan, HealthReport
# exactly as Notion "Architecture & contracts" §7.
```

## 3. Database (`schema.sql`)

```sql
CREATE TABLE IF NOT EXISTS events (
  id TEXT PRIMARY KEY, paypal_event_id TEXT UNIQUE, type TEXT NOT NULL, source TEXT NOT NULL,
  subject_id TEXT NOT NULL, data JSONB NOT NULL, verified BOOLEAN NOT NULL DEFAULT false,
  rejected BOOLEAN NOT NULL DEFAULT false, received_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS ledger (
  id BIGSERIAL PRIMARY KEY, kind TEXT NOT NULL, subject_id TEXT NOT NULL, summary TEXT NOT NULL,
  payload JSONB NOT NULL, prev_hash TEXT NOT NULL, hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS approvals (
  id TEXT PRIMARY KEY, agent TEXT, tool TEXT, args JSONB, reason TEXT, summary TEXT,
  amount_cents BIGINT, currency TEXT, status TEXT NOT NULL DEFAULT 'pending',
  decided_by TEXT, decided_at TIMESTAMPTZ, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS budgets (
  agent TEXT, tool TEXT, subject_id TEXT, window_start DATE, count INT NOT NULL DEFAULT 0,
  amount_cents BIGINT NOT NULL DEFAULT 0, PRIMARY KEY (agent, tool, subject_id, window_start));
CREATE TABLE IF NOT EXISTS agent_runs (
  id TEXT PRIMARY KEY, agent TEXT, event_id TEXT, event_type TEXT, status TEXT,
  steps JSONB NOT NULL DEFAULT '[]', output JSONB, started_at TIMESTAMPTZ DEFAULT now(), finished_at TIMESTAMPTZ);
CREATE TABLE IF NOT EXISTS invoices (id TEXT PRIMARY KEY, data JSONB NOT NULL, updated_at TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS shipments (id TEXT PRIMARY KEY, data JSONB NOT NULL, updated_at TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
```
Ledger append-only (never UPDATE/DELETE except demo tamper). Money = integer cents + ISO currency; "600.00" strings only in `paypal/client.py`.

## 4. SKJ modules

### M1 config.py
`Settings(BaseSettings)` with every var from `.env.example`. `agents_enabled: list[str]` parsed from CSV. Validator: `paypal_mode == "live"` → raise. `get_settings()` cached. Kill switch effective = env `KILL_SWITCH` OR `settings` row `kill_switch=true`.

Router table (also here):
```py
ROUTES = {"invoice.sent":"collector","invoice.overdue":"collector","email.received":"sentinel",
  "payment.captured":"guardian","shipment.created":"guardian","delivery.confirmed":"guardian",
  "dispute.created":"defender","dispute.updated":"defender"}
```

### M3 ledger.py
- `seal(kind, subject_id, summary, payload) -> LedgerEntry`: in one tx, `pg_advisory_xact_lock(42)`, read last hash (genesis `"0"*64`), `hash = sha256(prev_hash + canonical_json({kind,subject_id,summary,payload,created_at}))`, `canonical_json = json.dumps(sort_keys=True, separators=(",",":"), default=str)`. `created_at` generated in Python (UTC iso) and inserted, so hash is reproducible.
- `verify() -> {"ok","checked","broken_at"}`: walk by id, recompute.
- `find(kind=None, subject_id=None, limit=100, **payload_eq)` newest first.
- Test: seal 3, tamper one char in payload via SQL, `verify()["broken_at"] == that id`.

### M4 paypal/
- `client.py`: `PayPalClient` with httpx (timeout 10 s), OAuth token cached until expiry, one refresh on 401, `PayPal-Request-Id` header on every POST. One method per tool name (§6 table). Cents → "600.00" here.
- `fake.py`: same method names, returns JSON from `fixtures/paypal/<tool>.json` (fallback `{}`), records calls in a list for tests.
- `get_client()` returns fake or sandbox by `PAYPAL_MODE`.

### M5 webhooks.py + events.py
- `POST /webhooks/paypal`: call verify-webhook-signature (fake mode: trust); dedupe on `paypal_event_id`; map PayPal type → our `EventType`; `store_event`; return 200; `BackgroundTasks.add_task(route, event)`.
- `route(event)`: seal `kind="event"`; if type in ROUTES and agent in `agents_enabled` → `agents.<name>.handle(event, AgentContext(agent, run_id))`, write `agent_runs`.
- Unverified → `rejected=true`, not routed.

### M6 gateway
```py
def call(agent, tool, args, reason) -> Decision:
  # order: kill switch → agent enabled → allowlist → arg validation → caps (FOR UPDATE) → approval rule → execute → seal
```
`rules.py`:
```py
ALLOW = {"collector": {"get_invoice","list_invoices","send_invoice_reminder"},
  "sentinel": {"get_invoice","list_invoices","list_transactions"},
  "guardian": {"create_shipment_tracking","get_shipment_tracking","update_shipment_tracking"},
  "defender": {"list_disputes","get_dispute","send_dispute_message","provide_dispute_evidence",
               "make_dispute_offer","accept_dispute_claim"}}
ALWAYS_APPROVE = {"provide_dispute_evidence","make_dispute_offer","accept_dispute_claim"}
CAPS = {("collector","send_invoice_reminder"): 2}   # per subject per 7 days
def needs_approval(agent, tool, args) -> bool  # ALWAYS_APPROVE, first send_dispute_message, first reminder to new client, amount_cents >= threshold
def validate(agent, tool, args) -> str | None   # e.g. offer amount > disputed amount → error
```
HOLD → insert approval, return `approval_id`. `approve(approval_id, by)` → execute stored call (skip approval check, keep kill switch), seal `kind="approval"`. `reject` → seal. Every outcome sealed as `kind="decision"`.

### M7 llm.py
`complete(system, user, schema: type[BaseModel]) -> BaseModel`. Provider by `LLM_PROVIDER`; `fake` returns `fixtures/llm/<schema.__name__>.json`. Temp 0.2. Parse JSON → `schema.model_validate`; fail → one retry with error appended; fail again → raise `LLMError`. Log tokens + latency.

### M8 api.py / demo.py
Every route in Notion §9, `Depends(basic_auth)` (`secrets.compare_digest` vs `CONSOLE_PASSWORD`). Demo routes return 404 unless `DEMO_MODE`. Response shapes = mocks in [team/B_console.md](team/B_console.md#mocks).

### M18 deploy
Dockerfile multi-stage: node builds `frontend/dist`, python runs `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. `render.yaml`: web + Postgres. CI: `pytest` against service Postgres, `npm ci && npm run build`.

## 5. Teammate A modules (summary — full in team/A_agents.md)

| Module | Entry | Output | Done when |
|---|---|---|---|
| `agents/base.py` | `AgentContext(agent, run_id)` | tool / llm / ledger_find / log | wraps gateway.call, llm.complete, ledger.find; log appends to `agent_runs.steps` |
| Sentinel | `handle(event, ctx)` | `SentinelVerdict` | 20 emails: 0 scams marked legit, ≤2 false alarms |
| Defender | `handle(event, ctx)` | `EvidencePack` | 8 disputes correct; every fact cites ledger id |
| Collector | `handle(event, ctx)` | `CollectorPlan` | 10 reminders pass rubric |
| Guardian | `handle(event, ctx)` | `HealthReport` | tracking added in one event; facts cited |
| Evals | `python -m evals.run` | table | accuracy, false alarms, invalid JSON, latency |

## 6. Teammate B modules (summary — full in team/B_console.md)

Screens 1–10 against `/api/*`, mocks in `frontend/src/mocks/` until 11-05, then real API via Vite proxy.

## 7. Tests SKJ owns

`test_ledger.py` (tamper detect), `test_gateway.py` (allow/hold/deny/kill, cap), `test_config.py` (live refused), `test_webhooks.py` (dedupe, unverified not routed).
