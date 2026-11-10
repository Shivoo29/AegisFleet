# Setting up AegisFleet

This guide gets AegisFleet running on your machine, first with **no accounts or keys** (fake PayPal, fake AI),
then optionally with real AI models and a real PayPal sandbox. Allow about 15 minutes.

- [1. Prerequisites](#1-prerequisites)
- [2. Quick start (no keys)](#2-quick-start-no-keys)
- [3. Use real AI models](#3-use-real-ai-models-optional)
- [4. Use the PayPal sandbox](#4-use-the-paypal-sandbox-optional)
- [5. Connect an AI agent over MCP](#5-connect-an-ai-agent-over-mcp)
- [6. Tests and evals](#6-tests-and-evals)
- [7. Configuration reference](#7-configuration-reference)
- [8. Troubleshooting](#8-troubleshooting)

> **Secrets:** `.env` holds your passwords and API keys. It is git-ignored; keep it that way. Never commit it,
> paste it into chats, or screenshot it.

---

## 1. Prerequisites

| Tool | Version | Check |
|---|---|---|
| Git | any | `git --version` |
| Python | 3.12+ (on Windows, tick **Add python to PATH**) | `python --version` |
| Node.js | 20+ (LTS) | `node --version` |
| Docker | Docker Desktop or Docker Engine, running | `docker --version` |

Docker only runs the local PostgreSQL. Any Postgres 14+ works instead: point `DATABASE_URL` at it.

## 2. Quick start (no keys)

```bash
git clone https://github.com/Shivoo29/AegisFleet.git
cd AegisFleet
cp .env.example .env            # Windows PowerShell: copy .env.example .env
docker compose up -d db         # PostgreSQL 16 on localhost:5432
```

**Backend** (terminal 1):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q                       # all tests should pass
uvicorn app.main:app --reload   # http://localhost:8000/healthz -> {"ok":true}
```

**Frontend** (terminal 2):

```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173 (proxies /api, /mcp and /webhooks to :8000)
```

Log in with username **`dev`** and password **`dev`** (`CONSOLE_PASSWORD` in `.env`). Start with
**Demo → Reset demo state**, then follow the guided tour.

To serve everything from the backend instead (as in production): `cd frontend && npm run build`, then open
http://localhost:8000.

Frontend-only work without a backend: create `frontend/.env.local` with `VITE_USE_MOCKS=true`.

## 3. Use real AI models (optional)

All three providers have free tiers. Only one key is required; a provider without a key is skipped.

| Provider | Get a key | `.env` line |
|---|---|---|
| Groq (primary) | https://console.groq.com/keys | `GROQ_API_KEY=` |
| Google Gemini (fallback 1) | https://aistudio.google.com/apikey | `GEMINI_API_KEY=` |
| NVIDIA NIM (fallback 2) | https://build.nvidia.com | `NVIDIA_API_KEY=` |

Then set:

```
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-120b
LLM_FALLBACKS=gemini:gemini-3.5-flash,nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b
```

Restart the backend. If the primary is rate-limited or down, calls fall through the chain; if every
provider fails, agents fall back to their rules. `LLM_PROVIDER=fake` switches AI off again.

## 4. Use the PayPal sandbox (optional)

1. At https://developer.paypal.com, open **Apps & Credentials → Sandbox → Create App**. Copy the client ID
   and secret into `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET`.
2. Set `PAYPAL_MODE=sandbox`, and set `CONSOLE_PASSWORD` to something other than `dev` (the app refuses to
   start in sandbox mode with the default password). `PAYPAL_MODE=live` is always refused.
3. **Webhooks** need a public HTTPS URL. Expose the backend with a tunnel (for example
   `cloudflared tunnel --url http://localhost:8000` or `ngrok http 8000`). In your sandbox app, add a webhook
   for `https://<public-url>/webhooks/paypal` with these events: `INVOICING.INVOICE.PAID`,
   `INVOICING.INVOICE.REFUNDED`, `PAYMENT.CAPTURE.COMPLETED`, `PAYMENT.CAPTURE.REFUNDED`,
   `CUSTOMER.DISPUTE.CREATED`, `CUSTOMER.DISPUTE.UPDATED`, `CUSTOMER.DISPUTE.RESOLVED`. Copy its ID into
   `PAYPAL_WEBHOOK_ID`. Every incoming event is checked with PayPal's `verify-webhook-signature` before it
   is used.
4. Restart the backend. **Demo → Real PayPal invoice** issues a real sandbox invoice; pay it as a sandbox
   buyer (a US personal sandbox account works best) or use **Record payment (backup)**.

Without step 3 everything else works, but invoices never turn *paid* locally, because PayPal can't reach
`localhost`.

## 5. Connect an AI agent over MCP

The backend serves MCP at `http://localhost:8000/mcp`. In the console, **Demo → Connect any AI agent → Get
my MCP link** gives a URL with a signed token (valid 14 days) and the setup steps for ChatGPT, Claude,
Claude Code, Gemini CLI, Antigravity, Cursor, VS Code and Codex. Clients that support headers can use
`Authorization: Basic <base64 of dev:dev>` instead. Full per-client config: [README](README.md#-connect-any-ai-agent-mcp).

Hosted clients (ChatGPT, Claude.ai) can't reach `localhost`. Use the live site's link, or a tunnel as in
step 4. To test without an AI: `npx @modelcontextprotocol/inspector`.

## 6. Tests and evals

```bash
cd backend
pytest -q                                   # unit + integration tests (needs the database)
python -m evals.run --agent all --reset     # labelled agent suites; uses your LLM_PROVIDER
python ../scripts/export_openapi.py         # refresh docs/api/openapi.json after an API change
```

`--reset` clears the local database tables first. Evals run offline with `LLM_PROVIDER=fake`, or against
real models with keys from step 3. The latest real-model run is in [`docs/evals/`](docs/evals/).

## 7. Configuration reference

| Variable | Default | Meaning |
|---|---|---|
| `DATABASE_URL` | `postgresql://aegis:aegis@localhost:5432/aegis` | Postgres connection string |
| `PAYPAL_MODE` | `fake` | `fake` (fixtures) or `sandbox`; `live` is refused |
| `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_WEBHOOK_ID` | empty | Sandbox app credentials and webhook ID |
| `LLM_PROVIDER`, `LLM_MODEL`, `LLM_FALLBACKS` | `fake` | Primary model and the fallback chain |
| `GROQ_API_KEY`, `GEMINI_API_KEY`, `NVIDIA_API_KEY` | empty | Model provider keys |
| `AGENTS_ENABLED` | all four | Comma list of built-in agents allowed to act |
| `EXTERNAL_AGENTS_ENABLED` | `true` | Let outside AI agents act over MCP |
| `APPROVAL_THRESHOLD_CENTS` | `10000` | Money out at or above this waits for a human ($100) |
| `KILL_SWITCH` | `false` | `true` stops every agent action (also toggled in the console) |
| `PLAN_RUNNER` | `true` | Run agents' planned actions when they come due |
| `CONSOLE_PASSWORD` | `dev` | Password for user `dev` |
| `JUDGE_PASSWORD` | empty | Password for user `judge`; empty disables that login |
| `DEMO_MODE` | `true` | Enables the `/api/demo/*` story beats |

## 8. Troubleshooting

| Symptom | Fix |
|---|---|
| `PoolTimeout` or `connection refused` | The database isn't running: `docker compose up -d db` |
| `ModuleNotFoundError` | Activate the virtualenv (step 2) and `pip install -r requirements.txt` |
| Cannot connect to the Docker daemon | Start Docker Desktop and wait until it's running |
| Port 5432 already in use | Stop the other Postgres, or change the port in `docker-compose.yml` and `DATABASE_URL` |
| Login says wrong password | Use username `dev` (or `judge`), and the password from `.env` |
| "Set a real CONSOLE_PASSWORD" on start | You set `PAYPAL_MODE=sandbox`; change `CONSOLE_PASSWORD` from `dev` |
| Sandbox invoice never turns paid | PayPal can't reach your machine; set up the tunnel and webhook (step 4) |
| AI errors 401 / 429 | 401: wrong key or a typo in `.env`. 429: rate limit; the fallback chain takes over |
| `.env` changes do nothing | Save the file and restart the backend |
| `.env` appears in `git status` | Don't commit it; check `.gitignore` |

`.env` format: one `NAME=value` per line, no spaces around `=`, no quotes; anything after `#` is a comment.

## Contributing

Open an issue or a pull request against `main`. Run `pytest -q` and `npm run build` before you push; CI runs
both.
