# Devpost submission text

Paste each section into the matching Devpost field.

---

## Project name
AegisFleet

## Tagline
AI agents that help small sellers get paid and stay paid, while only rules or a human ever move money.

## Inspiration
Solo sellers on PayPal lose money in three quiet ways: fake "payment received" emails that trick them into shipping, "item not received" disputes they can't answer in time, and unpaid invoices nobody chases. AI can do this paperwork. But nobody should let a language model click "refund" on their behalf. We wanted agents that are useful *and* safe to hand money-adjacent work to.

## What it does
AegisFleet watches a seller's PayPal activity and runs AI agents behind a guardrail gateway:

- **Sentinel** reads suspicious "you got paid" emails and checks them against *verified* PayPal payments in the ledger. Lookalike domains, urgency, off-platform requests and amount mismatches are flagged, and the seller gets a plain-words verdict.
- **Defender** answers buyer disputes. It gathers the sealed payment, tracking and delivery records, classifies the claim, drafts the evidence, and recommends provide evidence, offer a refund, or accept. Every fact cites a ledger entry.
- **Collector** chases overdue invoices. It scores risk from invoice age and buyer history, chooses a tone and action with deterministic rules, counts prior reminders in the ledger, and drafts a capped reminder. It cannot change the amount, grant a discount or waive a fee, and it can only send a reminder through the gateway, capped at 2 per invoice per week.
- **Guardian** keeps PayPal shipment tracking in sync (registers tracking on shipment, marks it delivered) and scores account health from ledger facts: open disputes, refund rate, tracking coverage and sales spikes. The score is rule-based; AI only writes the recommendations, and every appeal-pack line cites a ledger entry.
- **The gateway** sits between every agent and PayPal. It checks the kill switch, a per-agent allowlist, argument validation and weekly caps, then **holds** anything that touches money until a human approves it in the console. An agent tricked into a refund is denied, and the attempt is recorded.
- **The Proof Ledger** hash-chains every event, decision and approval. Editing any past record breaks verification at that exact entry.

The console (React, AG Grid, Bryntum) shows money at risk, approvals, the ledger, agent activity, disputes and invoices, with a one-click demo panel.

## How we built it
- **PayPal (sandbox):** Invoicing v2 (create, send, record payment), Webhooks (registration and `verify-webhook-signature` on every event), Disputes (get, message, provide evidence, make offer, accept claim), Shipment Tracking, Transaction Search and Payments refunds. The client does OAuth with token caching and a `PayPal-Request-Id` on every write, so retries never double-act.
- **AI:** one OpenAI-compatible wrapper with a fallback chain (Groq → Gemini → NVIDIA NIM). Agents ask for JSON matching a Pydantic schema, invalid output is retried once with the error, and anything still invalid falls back to deterministic rules. Untrusted text such as emails and buyer messages is fenced in prompts and never followed as instructions.
- **Backend:** FastAPI, PostgreSQL (append-only ledger with advisory-lock sealing), signed session login.
- **Frontend:** React, Vite, TypeScript, AG Grid.
- **Evals:** labelled suites run against the real model: Sentinel 20/20 emails (0 scams missed, 0 false alarms), Defender 8/8 disputes (0 uncited facts), Collector 10/10 invoices, and 6/6 prompt-injection fixtures (0 tool calls, every disallowed tool denied).
- **Hosting:** Render, from `render.yaml` (Docker web service plus managed Postgres, Singapore). Every push to `main` redeploys.

## Sponsor tools we built with
- **AG Grid Community:** the Proof Ledger and Invoices tables. The ledger re-verifies the hash chain every few seconds; after a tamper the broken record pins to the top in red and every record after it is marked unproven. A link column shows ✓/✕ for each hash link, new records flash as they're sealed, clicking a row opens its full seal (both hashes and the raw payload), and the audit trail exports to CSV. Invoices flash when PayPal's signed webhook marks one paid, show an overdue bar and a pinned totals row, and link to each PayPal payment page.
- **Render:** the whole app (FastAPI, the React console, the docs portal) and its Postgres database run from one blueprint, with the PayPal sandbox and Groq → Gemini → NVIDIA chain wired through Render env vars. A GitHub Actions ping keeps the free instance awake for judges.
- **Bryntum Scheduler:** a Timeline tab puts every agent run, every action waiting on the seller's approval, overdue invoices and PayPal's dispute response deadlines on one schedule, with a live "now" line, so the seller sees at a glance what's due before PayPal decides for them.
- **APIMatic:** our FastAPI spec, typed and described to APIMatic's linter (SDK readiness 99/100, AI-tool readiness 98/100), generates a docs portal with a live playground and Python/TypeScript/C# samples, plus Python and TypeScript SDKs committed in `apimatic/sdk/`. The portal is served at https://aegisfleet.solvor.co.in/docs, with `llms.txt` so a coding agent can build on AegisFleet.

## Challenges we ran into
- Making AI useful without trusting it. We settled on a rule: AI drafts, classifies and recommends, and only deterministic rules or a human approval execute a PayPal call.
- Free-tier rate limits during evals, solved with a provider fallback chain.
- Sandbox checkout failing for an India-region buyer account. A US sandbox buyer works, and we kept a "record payment" path that fires the same signed webhook.

## Accomplishments that we're proud of
- A real sandbox invoice, paid through PayPal checkout, arrives as a signature-verified webhook and is sealed into a tamper-evident ledger within about a minute.
- Prompt-injected refund attempts are denied by design, not by prompt wording.
- Every claim an agent makes about money points at a specific ledger entry.

## What we learned
Guardrails belong outside the model. A small gateway with allowlists, caps and human approval made the agents far easier to trust than any prompt instruction could.

## What's next
- Run Collector on a daily schedule instead of on each `invoice.overdue` event.
- Move from sandbox to production behind the same gateway, with per-seller limits.

---

## Built with
python, fastapi, postgresql, react, typescript, vite, ag-grid, bryntum, render, apimatic, paypal-invoicing, paypal-webhooks, paypal-disputes, paypal-shipment-tracking, groq, gemini, nvidia-nim

## Tools used (AI)
| Tool | Model | How we use it |
|---|---|---|
| Groq | `openai/gpt-oss-120b` | Primary model for Sentinel (scam verdict), Defender (dispute classification and evidence notes), Collector (reminder wording) and Guardian (health recommendations). JSON output validated against Pydantic schemas. |
| Google Gemini API | `gemini-3.5-flash` | First fallback when Groq is rate-limited or errors. |
| NVIDIA NIM | `nemotron-3.5-super-vl-120b-a12b` | Second fallback. |
| AG Grid Community | – | Proof Ledger table, filtering, and highlighting the broken row after tampering. |

The models never call PayPal. They return structured recommendations; the gateway decides what runs.

## Links
- Live demo: https://aegisfleet.solvor.co.in
- API docs and SDKs (APIMatic): https://aegisfleet.solvor.co.in/docs
- Code: https://github.com/Shivoo29/AegisFleet (MIT)
- Video: `<YouTube link>`

## Testing instructions (judges only)
> Open https://aegisfleet.solvor.co.in and log in with username `judge`, password `<JUDGE_PASSWORD>`.
> 1. A short guide points at each step. Start with **Demo → Reset** to load the scenario.
> 2. **Real PayPal invoice** issues a real sandbox invoice. To pay it, use the sandbox buyer `<US sandbox buyer email>` / `<password>`, or click **Record payment (backup)**. The invoice turns *paid* within about a minute.
> 3. Try **Fake payment email**, **Replay injection** and **Tamper**, then check Activity, Approvals and Ledger.
> 4. Reset any time. Nothing real is connected: PayPal runs in sandbox, and live mode is refused in code.
>
> To run locally with no keys: see `SETUP.md` (fake PayPal and fake AI modes).
