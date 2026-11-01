# AegisFleet

**Stop losing money to fake payments, held funds, and friendly-fraud disputes.**
AegisFleet runs 4 AI agents (Sentinel, Defender, Collector, Guardian) behind a
guardrail gateway. AI may draft, classify, and recommend — only rules or a
human move money.

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