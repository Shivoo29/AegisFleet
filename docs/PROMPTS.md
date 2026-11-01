# Agent prompts (OpenCode / Antigravity)

Every prompt assumes the agent runs at the repo root and can read `docs/`. Rule for all: **do not commit, do not push**. SKJ (via Claude) reviews, then commits.

---

## 0. Base project setup (OpenCode, run once, by SKJ)

```
You are setting up the base skeleton of AegisFleet. Read docs/HLD.md and docs/LLD.md fully first; they are the spec. Build ONLY the skeleton + frozen contract stubs so two teammates can start work on branches. Do not implement business logic beyond what is listed. Do not git commit or push.

Create exactly this:

ROOT
- .gitignore (python, node, .env, .venv, dist, __pycache__, .pytest_cache)
- .env.example — exactly the vars in docs/LLD.md / Notion §11 with the default values shown (PAYPAL_MODE=fake, LLM_PROVIDER=fake, DEMO_MODE=true, CONSOLE_PASSWORD=dev, DATABASE_URL=postgresql://aegis:aegis@localhost:5432/aegis, AGENTS_ENABLED=collector,sentinel,guardian,defender, APPROVAL_THRESHOLD_CENTS=10000, KILL_SWITCH=false, others empty)
- docker-compose.yml — one service `db`: postgres:16, user/pass/db aegis, port 5432, named volume
- LICENSE (MIT, "AegisFleet contributors", 2026)
- README.md — one-line pitch + the "First run" commands from below
- .github/CODEOWNERS: `* @Shivoo29`
- .github/pull_request_template.md: sections What / Why / How to test / Screenshots / Checklist (No secrets, no live PayPal; Money moves go through gateway; Tests or evals updated)
- .github/workflows/ci.yml: on pull_request + push to main. Job backend: python 3.12, postgres:16 service, `pip install -r backend/requirements.txt`, `cd backend && pytest -q` with DATABASE_URL set to the service. Job frontend: node 20, `cd frontend && npm ci && npm run build`.

BACKEND (backend/)
- requirements.txt: fastapi, uvicorn[standard], pydantic>=2, pydantic-settings, psycopg[binary,pool]>=3.2, httpx, pytest  (pin current stable major versions)
- pytest.ini: testpaths=tests, pythonpath=.
- app/__init__.py
- app/config.py: pydantic-settings Settings with every env var typed; agents_enabled parsed from comma string to list[str]; model_validator that raises if paypal_mode == "live"; paypal_mode Literal["fake","sandbox","live"]; get_settings() with lru_cache; ROUTES dict exactly as docs/LLD.md §4 M1.
- app/models.py: every Pydantic model from docs/LLD.md §2 AND agent outputs SentinelVerdict, Fact, EvidencePack, CollectorPlan, HealthReport with the exact fields from docs/team/A_agents.md / Notion contracts §7 (copy field names and Literal values exactly).
- app/schema.sql: exactly docs/LLD.md §3.
- app/db.py: psycopg_pool.ConnectionPool opened lazily from settings.database_url, `conn()` context manager yielding a connection with dict_row, `init_schema()` executing schema.sql.
- app/ledger.py: signatures seal / verify / find per LLD §4 M3 — IMPLEMENT FULLY (it is small): advisory xact lock, genesis "0"*64, canonical json, created_at generated in python UTC.
- app/llm.py: `class LLMError(Exception)`; `complete(system, user, schema)`; implement only the fake provider (loads fixtures/llm/<SchemaName>.json relative to repo root, validates with schema); other providers raise NotImplementedError("set at M0").
- app/paypal/__init__.py, client.py (class PayPalClient: __init__ + one method stub per tool name in LLD §4 M6 ALLOW plus create_invoice, send_invoice, create_refund, verify_webhook_signature; each raises NotImplementedError), fake.py (class FakePayPal: __getattr__ returning a function that records (tool, args) in self.calls and returns json from fixtures/paypal/<tool>.json or {}), get_client() picking by settings.paypal_mode.
- app/paypal/webhooks.py: APIRouter with POST /webhooks/paypal returning {"ok": true} (TODO body).
- app/gateway/__init__.py, rules.py (ALLOW, ALWAYS_APPROVE, CAPS exactly as LLD; needs_approval and validate stubs returning False / None), gateway.py (`call(agent, tool, args, reason) -> Decision` implemented MINIMALLY: kill switch → agent enabled → allowlist → validate → needs_approval→hold (insert approvals row) → execute via get_client() → seal decision. Skip caps with a `# TODO(SKJ): caps FOR UPDATE` comment. Plus approve(approval_id, by) and reject(approval_id, by) stubs raising NotImplementedError).
- app/events.py: store_event(event) inserting into events; route(event): seal kind="event", look up ROUTES, if enabled import app.agents.<name> and call handle(event, AgentContext(name)), store agent_runs row. Wrap agent call in try/except that marks run failed.
- app/agents/__init__.py, base.py (AgentContext exactly as docs/team/A_agents.md "Interface" — implemented, thin wrappers; log appends {"kind","summary"} to self.steps; load_prompt(agent)), run.py (CLI: argv agent name + json path → Event(type from file "type" field or default per agent, source="console", subject_id from file or "test", data=file json, verified=False, id uuid) → print handle(...).model_dump_json(indent=2)), sentinel.py / defender.py / collector.py / guardian.py each with `def handle(event, ctx)` returning a safe default output model (Sentinel: verdict "unsure" etc.) and a `# TODO(A)` line, prompts/<agent>.md with "version: 0" line.
- app/api.py: APIRouter prefix /api, HTTP Basic dependency using secrets.compare_digest against settings.console_password (any username). Every route from docs/team/B_console.md "Screens" table and Notion §9, returning the shapes in docs/team/B_console.md types. Implement: /summary (counts from DB, chain_ok from ledger.verify), /ledger, /ledger/verify, /approvals, /runs, /killswitch GET+POST (settings table), /inbox POST (create email.received event, store, BackgroundTasks route, return {"run_id"}). Others: return [] or {} with `# TODO(SKJ)`.
- app/demo.py: APIRouter prefix /api/demo; dependency raising 404 unless settings.demo_mode; GET /status → {"demo": true}; POST endpoints scam_email, delivered, replay_injection, tamper, reset as TODO stubs returning {"ok": true}.
- app/main.py: FastAPI app; on startup call init_schema() (wrap: log and continue if DB unreachable? NO — fail loudly); include routers; GET /healthz → {"ok": true}; if ../frontend/dist exists mount StaticFiles(html=True) at "/" AFTER routers.
- tests/conftest.py: fixture that sets env PAYPAL_MODE=fake LLM_PROVIDER=fake, inits schema, TRUNCATEs all tables before each test.
- tests/test_config.py: live mode raises.
- tests/test_ledger.py: seal 3 entries, verify ok; UPDATE one payload by SQL; verify broken_at == that id.
- tests/test_gateway.py: kill switch → deny; unknown tool → deny; sentinel calling create_refund → deny; defender provide_dispute_evidence → hold with approval row; collector get_invoice → allow.
- tests/test_healthz.py using fastapi TestClient.

FIXTURES
- fixtures/paypal/.gitkeep, fixtures/llm/SentinelVerdict.json (valid unsure verdict), fixtures/emails/fake_payment_01.json ({"type":"email.received","subject_id":"INV-0007","from":"service@paypa1-support.com","subject":"Payment received","body":"You have received $600.00 ... ship now to release funds"}).

SCRIPTS
- scripts/__init__.py, scripts/replay.py (stub: reads a json file, POSTs to /webhooks/paypal), seed_demo.py and reset_demo.py stubs.

FRONTEND (frontend/) — Vite React TS
- package.json with react 18, react-dom 18, ag-grid-community + ag-grid-react (same major), vite, @vitejs/plugin-react, typescript. Scripts dev/build/preview. Generate package-lock.json by running npm install.
- vite.config.ts with proxy /api and /webhooks → http://localhost:8000.
- index.html, tsconfig.json, src/main.tsx, src/App.tsx (header "AegisFleet" + tab bar listing the 10 screens from docs/team/B_console.md, each rendering a placeholder <h2>), src/api.ts, src/usePoll.ts, src/types.ts (copy from docs/team/B_console.md), src/theme.css, src/mocks/summary.json + approvals.json + runs.json (payloads from Notion §9 in docs/team/B_console.md mocks note).

DEPLOY
- Dockerfile: stage 1 node:20 builds frontend; stage 2 python:3.12-slim installs backend reqs, copies backend + frontend/dist + fixtures, CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} from /app/backend.
- render.yaml: one web service (docker), one Postgres database, env vars from .env.example with sync:false for secrets.

VERIFY before you stop (show me the output):
1. docker compose up -d db
2. cd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && pytest -q   → all pass
3. uvicorn app.main:app & ; curl localhost:8000/healthz ; curl -u x:dev localhost:8000/api/summary ; kill it
4. python -m app.agents.run sentinel ../fixtures/emails/fake_payment_01.json
5. cd ../frontend && npm install && npm run build
Fix anything that fails. Keep code minimal, no extra libraries, no ORM, no abstractions beyond what is listed. Do NOT git commit.
```

---

## 1. Teammate A starter (give to their OpenCode/Antigravity on branch `a/datasets-v1`)

```
You are working on AegisFleet as Teammate A (AI Agents). Read docs/HLD.md, docs/LLD.md, docs/team/A_agents.md first. You may ONLY edit: backend/app/agents/**, backend/evals/**, fixtures/emails|disputes|invoices|injection|llm/**, and add tests under backend/tests/test_agents_*.py. Never import paypal/, db, or gateway inside agents — only use ctx (AgentContext).

Today's task (branch a/datasets-v1, then a/sentinel-v1):
1. Write datasets per "Datasets" table in docs/team/A_agents.md: 20 emails (10 scam covering: fake payment received, fake support phone in invoice note, overpayment refund, phishing login, ship-first; 10 legit realistic PayPal notifications and client messages), 8 disputes (scenarios listed in A_agents.md), 6 injection emails. No real customer data.
2. Write agents/prompts/sentinel.md (version: 1): role, untrusted-text rule, red flags list, output JSON schema, ≤3-sentence explanation.
3. Implement agents/sentinel.py per the Sentinel LLD steps, including the deterministic guard (no verified payment in ledger → never "legit").
4. Implement backend/evals/run.py printing the table: agent | n | accuracy | false_alarms | invalid_json_pct | avg_latency_ms.
5. Add tests/test_agents_sentinel.py with LLM_PROVIDER=fake proving the guard overrides a "legit" LLM answer when no verified payment exists.
Run pytest and `python -m evals.run`; show output. Do not commit.
```

## 2. Teammate B starter (branch `b/shell`)

```
You are working on AegisFleet as Teammate B (Console). Read docs/HLD.md and docs/team/B_console.md first. You may ONLY edit frontend/** and docs/ images. Dependencies: only what package.json already has (React, AG Grid). No router lib, no UI kit, no state lib, no websockets.

Today's task (branch b/shell):
1. Design tokens in src/theme.css: calm fintech, one accent colour, green/amber/red status meanings per B_console.md.
2. App shell: Header (title + shield mark, kill switch toggle with confirm dialog, chain badge, pending approvals count from /api/summary), tab nav for the 10 screens.
3. api.ts: get/post with VITE_USE_MOCKS=true reading src/mocks/*.json; else fetch same-origin /api. usePoll(fn, 3000).
4. Write all mocks listed in B_console.md "Files" using types.ts shapes (Riya's jewellery shop, USD, dispute PP-D-12345, invoice INV-0007).
5. Every screen placeholder shows loading / empty / error states.
6. format.ts: money(cents, ccy) right-aligned display, e.g. "$600.00 USD".
Run `npm run build` and `VITE_USE_MOCKS=true npm run dev`; describe what renders. Do not commit.
```

---

## 3. SKJ module prompts (your own work, on `main`)

Use one at a time; Claude reviews each before commit.

**3a ledger + webhooks (11-03/05)**
```
Read docs/LLD.md §4 M3 and M5. Harden app/ledger.py (already implemented) and implement app/paypal/webhooks.py fully: verify signature via client.verify_webhook_signature (fake mode trusts), dedupe on paypal_event_id (ON CONFLICT DO NOTHING → return 200 without routing), map PayPal event types to our EventType, store unverified as rejected and never route, BackgroundTasks route. Add tests/test_webhooks.py (dedupe, unverified not routed). Only edit those files. Run pytest. No commit.
```

**3b gateway (11-04)**
```
Read docs/LLD.md §4 M6. Complete app/gateway/: caps with SELECT ... FOR UPDATE on budgets (7-day window per subject), needs_approval (ALWAYS_APPROVE, first send_dispute_message per dispute, first send_invoice_reminder to a new client, amount_cents >= APPROVAL_THRESHOLD_CENTS), validate (offer amount <= disputed amount), approve()/reject() executing the stored call and sealing. PayPal-Request-Id = decision id. Extend tests/test_gateway.py: cap hit → deny, approve → allow + sealed. Run pytest. No commit.
```

**3c paypal client (11-05/06)**
```
Read docs/LLD.md §4 M4 and Notion §10 table copied there. Implement app/paypal/client.py against PayPal sandbox REST with httpx (timeout 10 s): OAuth client-credentials with cached token until expiry, one retry on 401, PayPal-Request-Id on every POST, cents→"600.00" conversion here only. Methods: invoicing v2 (create_invoice, send_invoice, get_invoice, list_invoices, send_invoice_reminder), /v1/shipping/trackers (create/get/update_shipment_tracking), disputes v1 (list/get_dispute, send_dispute_message, provide_dispute_evidence, make_dispute_offer, accept_dispute_claim, require_evidence, adjudicate), list_transactions, verify_webhook_signature. Unit test with httpx.MockTransport for token caching and 401 retry. No commit.
```

**3d api + demo + deploy (11-04 → 11-08)**
```
Read docs/LLD.md §4 M8, M18 and docs/team/B_console.md Screens table. Finish every TODO(SKJ) in app/api.py and app/demo.py returning exactly the TS types in B_console.md. demo: scam_email (POST a canned email via inbox path), delivered (create delivery.confirmed event), replay_injection (gateway.call("sentinel","create_refund",...) → must deny), tamper (UPDATE one ledger row payload), reset (truncate + reseed). Test each demo route in tests/test_demo.py. No commit.
```
