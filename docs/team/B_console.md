# Teammate B — Console, Demo & Story: HLD + LLD

Branch: `b/<topic>` (e.g. `b/ledger-grid`). PR to `main` with screenshot, SKJ reviews.

## HLD

You own: `frontend/**`, `docs/architecture.png`, screenshots, video, Devpost draft, README visuals.

```mermaid
flowchart LR
  App --> Header[Header: kill switch, chain badge, approvals count]
  App --> Nav[Tabs]
  Nav --> Overview & Approvals & Ledger & Activity & Inbox & Disputes & Invoices & Health & Demo
  Screens --> api.ts --> |USE_MOCKS| mocks/*.json
  api.ts --> |else| /api via Vite proxy :8000
```

Stack: React 18, Vite, TS, AG Grid Community (every table). Plain `fetch`, `usePoll(fn, 3000)`. Deps: AG Grid only (tabs by state, no router unless SKJ agrees). Browser handles HTTP Basic prompt — never store password in localStorage.

Design: calm fintech, one accent colour, money right-aligned with currency, green = safe/verified, amber = needs approval, red = blocked/broken. Every agent action reads as a sentence. Empty / loading / error state on every screen. Own shield mark, no PayPal logo.

## LLD

### Files
```
frontend/
├── index.html, vite.config.ts (proxy /api,/webhooks → http://localhost:8000)
└── src/
    ├── main.tsx, App.tsx          tabs state, Header
    ├── api.ts                     get<T>(path), post<T>(path, body); USE_MOCKS = import.meta.env.VITE_USE_MOCKS === "true"
    ├── usePoll.ts                 hook: fetch every 3 s, returns {data, error, loading}
    ├── types.ts                   TS copies of contract models
    ├── format.ts                  money(cents, ccy), time()
    ├── theme.css                  tokens
    ├── mocks/                     summary.json, approvals.json, runs.json, ledger.json, verify.json,
    │                              invoices.json, disputes.json, dispute_detail.json, health.json, killswitch.json
    └── screens/ Overview, Approvals, Ledger, Activity, Inbox, Disputes, Invoices, Health, DemoPanel .tsx
```

### Types (`types.ts`) — mirror backend exactly
```ts
export type Summary = { money_at_risk_cents: number; currency: string; pending_approvals: number;
  open_disputes: number; overdue_invoices: number; health_score: number; kill_switch: boolean; chain_ok: boolean };
export type Approval = { id: string; agent: string; tool: string; summary: string; amount_cents: number | null;
  currency: string | null; reason: string; args: Record<string, unknown>; status: "pending"|"approved"|"rejected"; created_at: string };
export type LedgerEntry = { id: number; kind: "event"|"decision"|"agent_step"|"approval"|"note"; subject_id: string;
  summary: string; payload: unknown; prev_hash: string; hash: string; created_at: string };
export type Verify = { ok: boolean; checked: number; broken_at: number | null };
export type Run = { id: string; agent: string; event_type: string; status: string; started_at: string;
  steps: { kind: "llm"|"tool"|"note"; summary: string }[]; output: unknown };
export type Fact = { claim: string; ledger_entry_id: number };
export type EvidencePack = { dispute_id: string; reason: string; classification: "friendly_fraud"|"genuine"|"unclear";
  confidence: number; checklist: Record<string, boolean>; facts: Fact[]; note_to_paypal: string;
  recommended_action: "provide_evidence"|"offer_refund"|"accept_claim" };
export type SentinelVerdict = { verdict: "scam"|"legit"|"unsure"; confidence: number;
  matched_payment_entry_id: number | null; red_flags: string[]; explanation: string };
export type HealthReport = { score: number; factors: { name: string; value: unknown; impact: string; note: string }[];
  recommendations: string[]; appeal_pack: string | null };
```

### Mocks
Use payloads from Notion "Architecture & contracts" §9 verbatim for `summary.json`, `approvals.json`, `runs.json`. Invent the rest from the types above (Riya's jewellery shop, USD, dispute `PP-D-12345`, invoice `INV-0007`).

### Screens
| # | Screen | Endpoint | Done when |
|---|---|---|---|
| 1 | Header | `GET /api/summary`, `GET/POST /api/killswitch` | confirm dialog; badge red when `chain_ok=false` |
| 2 | Overview | `/api/summary`, `/api/runs?limit=10` | updates ≤ 3 s |
| 3 | Approvals | `GET /api/approvals?status=pending`, `POST /api/approvals/{id}/approve|reject` `{note}` | item leaves list, result shown |
| 4 | Ledger (AG Grid) | `/api/ledger?kind=&subject_id=&limit=`, `/api/ledger/verify` | filters; ✅ or highlight `broken_at` row |
| 5 | Activity | `/api/runs` | row expands to steps |
| 6 | Inbox | `POST /api/inbox` `{from, subject, body}` → `{run_id}`, then poll `/api/runs` | verdict card with red flags |
| 7 | Disputes | `/api/disputes`, `/api/disputes/{id}` → `{dispute, evidence_pack, approval_id}` | checklist ticks, facts link to ledger, approve button |
| 8 | Invoices (P1) | `/api/invoices`, `POST /api/shipments` `{invoice_id, carrier, tracking_number}` | risk, days overdue, ship-gate |
| 9 | Health (P1) | `/api/health` | score, factors, recs |
| 10 | Demo panel | `POST /api/demo/{scam_email|delivered|replay_injection|tamper|reset}` | shown only if `/api/demo/status` 200 |

## Timeline

| Date | Deliverable | Branch |
|---|---|---|
| 11-02 | Layout, tabs, tokens, api.ts, mocks | `b/shell` |
| 11-03 | Ledger grid + verify; Approvals (mock) | `b/ledger-approvals` |
| 11-04 | Activity; Disputes + evidence (mock) | `b/activity-disputes` |
| 11-05 | Real API (M1); approve works on Render | `b/real-api` |
| 11-06 | Inbox + Invoices | `b/inbox-invoices` |
| 11-07 | Overview, Header kill switch, Health, Demo panel, empty/error states | `b/overview-demo` |
| 11-08 | Rehearsal; video script v1 | — |
| 11-09 | Polish, screenshots | `b/polish` |
| 11-10 18:00 | Freeze; record | — |
| 11-11 18:00 | MP4 to SKJ; Devpost text + gallery | — |

## Done means
PR merged, `npm run build` green, screenshot in PR, screen works on mocks and on real API.
