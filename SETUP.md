# Setting up AegisFleet on your laptop

Follow this top to bottom once. It takes about 20 minutes. If a step fails, copy the
exact error message and send it in the group — don't guess.

> **Golden rule about secrets:** your `.env` file holds your passwords and API keys.
> Never commit it, never paste it in WhatsApp/Discord, never screenshot it.
> Git already ignores it, so `git add .` is safe — but double check `git status`
> never shows `.env`.

---

## 1. Install the tools (one time)

| Tool | Why | Get it | Check it works |
|---|---|---|---|
| Git | download the code | https://git-scm.com/downloads | `git --version` |
| Python 3.12 or newer | runs the backend | https://www.python.org/downloads/ (Windows: tick **"Add python to PATH"**) | `python --version` |
| Node.js 20 or newer | runs the console (frontend) | https://nodejs.org (LTS) | `node --version` |
| Docker Desktop | runs the database | https://www.docker.com/products/docker-desktop/ | `docker --version` |

After installing Docker Desktop, **open it once** and leave it running in the background.

---

## 2. Get the code

```bash
git clone https://github.com/Shivoo29/AegisFleet.git
cd AegisFleet
```

Already cloned it earlier? Just update instead:

```bash
cd AegisFleet
git checkout main
git pull
```

---

## 3. Make your `.env` file

The repo has a template called `.env.example`. You copy it to `.env` and fill in **your own** values.
Nobody sends you their `.env` — everyone makes their own.

**Mac / Linux:**
```bash
cp .env.example .env
```
**Windows (PowerShell):**
```powershell
copy .env.example .env
```

Open `.env` in VS Code. It looks like this. Here is what each line means:

| Line | What to put | Need to change? |
|---|---|---|
| `DATABASE_URL=...` | leave as is | No |
| `PAYPAL_MODE=fake` | leave `fake` — uses saved sample data, no PayPal account needed | No |
| `PAYPAL_CLIENT_ID=` / `PAYPAL_CLIENT_SECRET=` / `PAYPAL_WEBHOOK_ID=` | leave empty | No |
| `LLM_PROVIDER=fake` | `fake` = no AI calls, uses a saved answer. Fine to start. See step 3b to use real AI. | Optional |
| `LLM_MODEL=` / `LLM_FALLBACKS=` | only for real AI (step 3b) | Optional |
| `GROQ_API_KEY=` / `GEMINI_API_KEY=` / `NVIDIA_API_KEY=` | only for real AI (step 3b) | Optional |
| `AGENTS_ENABLED=...` | leave as is | No |
| `APPROVAL_THRESHOLD_CENTS=10000` | leave as is ($100) | No |
| `KILL_SWITCH=false` | leave as is | No |
| `CONSOLE_PASSWORD=dev` | leave `dev` on your laptop | No |
| `DEMO_MODE=true` | leave as is | No |

**That's it — with the defaults the whole app runs with zero keys.** Save the file (Ctrl+S).
An unsaved `.env` is the #1 reason things "don't work".

### Rules for editing `.env`
- One setting per line: `NAME=value`
- **No spaces** around `=` and **no quotes**: `GROQ_API_KEY=gsk_abc123` ✅ — `GROQ_API_KEY = "gsk_abc123"` ❌
- Exactly **one** `=` after the name. `NVIDIA_API_KEY==nvapi...` ❌ (this broke things for us once)
- Everything after `#` is a comment, ignored.

### 3b. (Teammate A only, when testing agents) Use real AI — all free

You need your **own** free keys. Takes 5 minutes each, no credit card.

| Provider | Where to get a key | Paste into |
|---|---|---|
| Groq (main, fastest) | https://console.groq.com/keys → **Create API Key** | `GROQ_API_KEY=` |
| Google Gemini (backup 1) | https://aistudio.google.com/apikey → **Create API key** | `GEMINI_API_KEY=` |
| NVIDIA NIM (backup 2) | https://build.nvidia.com → sign in → any model → **Get API Key** | `NVIDIA_API_KEY=` |

Then set these three lines exactly:
```
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-120b
LLM_FALLBACKS=gemini:gemini-3.5-flash,nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b
```
If Groq is busy or down, the app automatically tries Gemini, then NVIDIA.
Only Groq is required; a provider with an empty key is just skipped.

Want to go back to no-AI mode? Set `LLM_PROVIDER=fake`.

---

## 4. Start the database

Docker Desktop must be open. From the `AegisFleet` folder:

```bash
docker compose up -d db
```

Check: `docker ps` shows a row with `postgres:16`.
After a laptop restart, run the same command again (or `docker start aegisfleet-db-1`).

---

## 5. Backend (Python)

```bash
cd backend
python -m venv .venv
```
Activate it (you need this **every time** you open a new terminal):

- Mac / Linux: `source .venv/bin/activate`
- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
  (if Windows blocks it, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`)

Your prompt now starts with `(.venv)`. Then:

```bash
pip install -r requirements.txt
pytest -q
```
All tests should pass (green dots, no `F`). Then start the server:

```bash
uvicorn app.main:app --reload
```
Open http://localhost:8000/healthz — you should see `{"ok":true}`.
Leave this terminal running.

---

## 6. Frontend / console (Node)

Open a **second** terminal:

```bash
cd AegisFleet/frontend
npm install
npm run dev
```
Open http://localhost:5173. The browser asks for a login:
- **Username:** anything (e.g. your name)
- **Password:** `dev` (the `CONSOLE_PASSWORD` from your `.env`)

**Teammate B:** to build screens without the backend running, create `frontend/.env.local` containing:
```
VITE_USE_MOCKS=true
```
Delete that line (or set `false`) to talk to the real backend.

---

## 7. Daily workflow (how we use Git)

`main` is protected — you never push to it. Every feature is its own branch and PR.

```bash
git checkout main
git pull                          # get the latest
git checkout -b a/my-feature      # A uses a/..., B uses b/...
# ...work, then:
git add <the files you changed>
git commit -m "feat: short description"
git push -u origin a/my-feature
```
Open the PR on GitHub. SKJ reviews and merges.

Got review comments? **Fix on the same branch** and push again — the PR updates itself.
Don't open a new PR for fixes.

Main moved ahead while you worked? Update your branch:
```bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

---

## 8. Common problems

| You see | Fix |
|---|---|
| `PoolTimeout` / `connection refused` in tests | Database is off → `docker compose up -d db` |
| `ModuleNotFoundError: No module named 'psycopg'` (or any module) | venv not active → activate it (step 5) |
| `docker: command not found` / cannot connect to Docker daemon | Open Docker Desktop and wait till it says "running" |
| Port 5432 already in use | Another Postgres is running on your laptop — stop it, or ask SKJ |
| AI returns 401 | Wrong key or a typo in `.env` (extra `=`, space, quotes) |
| AI returns 429 | Free limit hit — wait a minute; the fallback providers kick in automatically |
| App refuses to start: "console password" | You changed `PAYPAL_MODE` from `fake` — set it back to `fake` |
| Changes in `.env` do nothing | Save the file, then stop the server (Ctrl+C) and start it again |
| `git status` shows `.env` | **Stop.** Don't commit. Tell SKJ. |

Still stuck? Send in the group: the command you ran + the full error text.
