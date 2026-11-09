# AegisFleet Frontend

React 18 + Vite + TypeScript + AG Grid Community.

## Screens (through Thursday)

| Screen | Status |
|--------|--------|
| Ledger + Verify chain | Done (mock) |
| Approvals inbox | Done (mock) |
| Activity feed | Done (mock) |
| Disputes + evidence pack | Done (mock) |
| Overview / Inbox / Invoices / Health / Demo | Placeholders (next days) |

## Run

```bash
npm install
VITE_USE_MOCKS=true npm run dev
```

Open http://localhost:5173

Mocks are opt-in with `VITE_USE_MOCKS=true`.

## Thursday: switch to real API

1. Backend must be running (local `:8000` or Render URL).
2. Set `VITE_USE_MOCKS=false` in `frontend/.env`:

```bash
VITE_USE_MOCKS=false
# optional if API is not same-origin via Vite proxy:
# VITE_API_BASE=https://your-render-url.onrender.com
```

3. Restart:

```bash
npm run dev
```

Vite proxies `/api` → `http://localhost:8000` when using the dev server.

## Build

```bash
npm run build
```

Output goes to `dist/` (served by the backend in production).
