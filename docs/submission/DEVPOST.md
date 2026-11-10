# Devpost submission text

Paste each section into the matching Devpost field. Fill the three `<...>` placeholders in Devpost itself;
never commit the judge password to the repo.

---

## Project name
AegisFleet

## Tagline
Let any AI agent bill and refund on PayPal safely: every action passes caps, human approval and a tamper-evident ledger.

## Inspiration
Everyone is building AI agents that spend and move money. Almost nobody is building the brakes. For a solo seller on PayPal, an agent that can click "refund" is one prompt injection away from emptying the account, and the same seller is already losing money to fake "payment received" emails, disputes they can't answer in time, and invoices nobody chases. We wanted agents a seller can actually hand money work to: useful, but unable to do anything the seller's rules don't allow, and unable to hide what they did.

## What it does
AegisFleet is a guardrail gateway between AI agents and a seller's PayPal account.

- **One way to PayPal.** Every agent action goes through the gateway: kill switch, a per-agent allowlist, argument checks, weekly caps, then a **hold for human approval** on refunds of $100 or more. Refunds can only go back to the buyer who paid, never for more than PayPal says they paid.
- **A Proof Ledger.** Every PayPal event, gateway decision, approval and plan is hash-chained. Edit any past record and verification points at that exact entry.
- **Any agent, over MCP.** AegisFleet is an MCP server. Connect Claude Code (or any MCP client) and it can issue real PayPal sandbox invoices, send reminders, check suspicious emails and refund buyers, but only through the gateway. We tested it live: the agent invoiced $150, PayPal's signed webhook marked it paid, the agent's $900 refund "to my other account" was denied, its $150 refund was held, the seller approved it in the console, and PayPal's refund webhook marked the invoice refunded.
- **Four built-in agents.** Sentinel checks "you've been paid" emails against verified PayPal payments, not against what the email says. Defender builds dispute evidence from the ledger and writes the note to PayPal, which is used only if every claim cites a real ledger entry. Collector chases overdue invoices with capped, polite reminders. Guardian syncs tracking and scores account health.
- **Agents plan ahead.** Collector books its own follow-up and final notice, Guardian books a carrier check, Defender books a re-check 48 hours before PayPal's dispute deadline. The seller sees them on a timeline and can drag any of them; when one comes due it runs through the same gateway, so a plan that breaks a rule is blocked, not run. When facts change (the invoice gets paid), the agents cancel the plans that no longer make sense.

The console (React, AG Grid, Bryntum) shows money at risk, approvals, the ledger, the agents' timeline, disputes and invoices, with a one-click demo panel and a guided tour.

## How we built it
- **PayPal (sandbox), used live:** Invoicing v2 (create, send, remind, record payment, record refund), Payments v2 capture refunds for invoices paid through PayPal, and Webhooks with `verify-webhook-signature` on every event (invoice paid and refunded, captures, disputes). The client does OAuth with token caching and a `PayPal-Request-Id` on every write, so a retry never double-acts.
- **PayPal, implemented but replayed in the demo:** Disputes (get, message, provide evidence, make offer, accept claim) and Shipment Tracking. The sandbox can't open a dispute on demand, so the demo's dispute and parcel are a replayed story; those calls run against recorded PayPal payloads and are labelled "simulated" in the ledger.
- **MCP:** the official MCP Python SDK, streamable HTTP at `/mcp`, eight tools, HTTP Basic with the console login. Outside agents act as their own gateway identity with their own allowlist and caps.
- **AI:** one OpenAI-compatible wrapper with a fallback chain (Groq → Gemini → NVIDIA NIM). Agents return JSON validated against Pydantic schemas; invalid output is retried once, then falls back to rules. Untrusted text (emails, buyer messages) is fenced and never followed as instructions. Rules decide anything that moves money; the model reads, flags, breaks ties and writes the words people read, and those words are checked before use.
- **Evals, real model, committed in `docs/evals/`:** Sentinel 20/20 emails (0 scams missed, 0 false alarms), Defender 8/8 disputes (0 uncited facts, 8/8 AI-written notes passed the citation check), Collector 10/10 invoices, prompt injection 6/6 (every disallowed tool call denied).
- **Backend:** FastAPI and PostgreSQL (append-only ledger sealed under an advisory lock), a plan runner, signed session login. 70+ tests and CI.
- **Hosting:** Render, from `render.yaml`. Every push to `main` redeploys.

## Sponsor tools we built with
- **Bryntum Scheduler:** the agents' timeline. Each agent has a row; the actions it has planned are dashed bars the seller can drag to a new time (the move is sealed in the ledger). Dropping one on "now" makes it run within seconds through the gateway, and the bar turns ✓, ⏸ (waiting for approval) or ✕ (blocked, with the gateway's reason in the tooltip). Approvals, overdue invoices and PayPal's dispute deadline sit on the same schedule.
- **AG Grid Community:** the Proof Ledger and Invoices tables. The ledger re-verifies the chain every few seconds; after a tamper the broken record pins to the top in red and everything after it is marked unproven. A link column shows ✓/✕ per hash link, new records flash as they're sealed, a row click opens the full seal, and the audit trail exports to CSV. Invoices flash when PayPal's webhook marks one paid or refunded, with an overdue bar and a pinned totals row.
- **APIMatic:** our OpenAPI spec, typed and described to APIMatic's linter (SDK readiness 99/100, AI-tool readiness 98/100), generates the docs portal at https://aegisfleet.solvor.co.in/docs (live playground, Python/TypeScript/C# samples, an MCP page and `llms.txt`) plus Python and TypeScript SDKs in `apimatic/sdk/`.
- **Render:** the app, the docs portal and Postgres run from one blueprint, with PayPal sandbox and model keys in Render env vars. A GitHub Actions ping keeps the instance awake for judges.

## Challenges we ran into
- Making AI useful without trusting it. The rule we kept: AI drafts, classifies and recommends; only the gateway's rules or a human approval execute a PayPal call.
- Letting outside agents in without opening a hole. They get their own identity in the gateway, a narrower allowlist, caps, and refunds bounded by the ledger's record of what the buyer actually paid.
- Free-tier rate limits during evals; the fallback chain absorbed them.
- Sandbox checkout failed for an India-region buyer account, so we kept a "record payment" path that fires the same signed webhook.

## Accomplishments that we're proud of
- An outside AI agent invoicing, getting paid and refunding on real PayPal sandbox, with the seller approving the money move and PayPal's own signed webhooks confirming each step.
- Prompt-injected refunds are denied by the gateway's rules, not by prompt wording.
- Every claim an agent makes about money points at a specific ledger entry, and the AI-written dispute note is thrown away if it doesn't.

## What we learned
Guardrails belong outside the model. A small gateway with allowlists, caps, human approval and a ledger made agents easier to trust than any prompt could, and it let us open the door to agents we didn't write.

## What's next
- Put PayPal's own Agent Toolkit and MCP server behind the same gateway, so any PayPal tool an agent calls gets caps, approvals and a ledger.
- Per-seller limits and production mode, behind the same rules.
- Buyer-side agents: let a shopper's agent request a refund or pay an invoice through AegisFleet, with the seller's rules deciding.

---

## Built with
python, fastapi, postgresql, mcp, react, typescript, vite, bryntum, ag-grid, apimatic, render, paypal-invoicing, paypal-payments, paypal-webhooks, paypal-disputes, groq, gemini, nvidia-nim

## Tools used (AI)
| Tool | Model | How we use it |
|---|---|---|
| Groq | `openai/gpt-oss-120b` | Primary model for all four agents: Sentinel's red flags, Defender's classification tie-breaks and its note to PayPal, Collector's reminder wording, Guardian's recommendations. JSON validated against Pydantic schemas. |
| Google Gemini API | `gemini-3.5-flash` | First fallback when Groq is rate-limited or errors. |
| NVIDIA NIM | `nemotron-3.5-super-vl-120b-a12b` | Second fallback. |
| Claude Code | – | Our coding assistant while building, and the outside agent we demo connecting over MCP. |

The models never call PayPal and never hold credentials. They return structured output; the gateway decides what runs.

## Links
- Live demo: https://aegisfleet.solvor.co.in
- MCP endpoint: https://aegisfleet.solvor.co.in/mcp
- API docs and SDKs (APIMatic): https://aegisfleet.solvor.co.in/docs
- Code: https://github.com/Shivoo29/AegisFleet (MIT)
- Video: `<YouTube link>`

## Testing instructions (judges only)
> Open https://aegisfleet.solvor.co.in and log in with username `judge`, password `<JUDGE_PASSWORD>`.
> 1. A short guide points at each step. Start with **Demo → Reset demo state**.
> 2. **Real PayPal invoice** issues a real sandbox invoice. Pay it as the sandbox buyer `<US sandbox buyer email>` / `<password>`, or click **Record payment (backup)**. It turns *paid* in Invoices within about a minute, via PayPal's signed webhook.
> 3. Run **Overdue invoice**, then open **Timeline**: Collector has planned a follow-up and a final notice. Drag the follow-up onto the red "now" line: it runs within seconds (✓). Drag the final notice there too: the gateway blocks it (✕, 2 reminders per week).
> 4. Try **Fake payment email**, **Replay injection** and **Tamper**, then check Activity, Approvals and Ledger.
> 5. Optional, with Claude Code: the Demo tab builds a `claude mcp add` command. Ask Claude to invoice a buyer, then to refund it; approve the refund in Approvals.
>
> Nothing real is connected: PayPal runs in sandbox and live mode is refused in code. To run locally with no keys, see `SETUP.md`.
