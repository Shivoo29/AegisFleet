# Devpost submission text

Paste each section into the matching Devpost field. Fill the `<...>` placeholders in Devpost itself; never
commit the judge password to the repo.

---

## Project name
AegisFleet

## Elevator pitch
AI agents that bill, chase and refund on PayPal for small sellers. Any AI can plug in over MCP, but big refunds wait for the seller and every move is sealed in a tamper-evident ledger.

## About the project

## Inspiration
Lots of teams are building AI agents that spend and move money, and very few are building the brakes. For a solo seller on PayPal, an agent that can click "refund" is one prompt injection away from emptying the account. The same seller is already losing money to fake "payment received" emails, disputes they can't answer in time, and invoices nobody chases. We wanted agents a seller could hand that work to: useful, unable to do anything the seller's rules don't allow, and unable to hide what they did.

## What it does
AegisFleet is a guardrail gateway between AI agents and a seller's PayPal account. Our demo seller is Riya, who sells jewellery from Jaipur to buyers in the US.

Every agent action goes through the gateway before it reaches PayPal. The gateway checks the kill switch, the agent's allowlist, the arguments and the weekly caps, and holds refunds of $100 or more until the seller approves them. A refund can only go back to the buyer who paid, and never for more than PayPal says they paid.

Every PayPal event, gateway decision, approval and plan is sealed in a hash-chained Proof Ledger. If anyone edits a past record, verification points at that exact entry.

Any AI agent can use it. AegisFleet is an MCP server, so ChatGPT, Claude, Gemini, Cursor or any other MCP client can connect with one link and issue real PayPal sandbox invoices, send reminders, check suspicious emails and refund buyers, always through the gateway. Each tool declares whether it is read-only or destructive, so a client can warn before a refund. We tested the whole loop live: the agent invoiced $150, PayPal's signed webhook marked it paid, the agent's $900 refund "to my other account" was denied, its $150 refund was held, the seller approved it in the console, and PayPal's refund webhook marked the invoice refunded.

Our own four agents work under the same rules:
- **Sentinel** checks "you've been paid" emails against verified PayPal payments instead of trusting what the email says.
- **Defender** builds dispute evidence from the ledger and writes the note to PayPal. The note is used only if every claim in it cites a real ledger entry.
- **Collector** chases overdue invoices with capped, polite reminders.
- **Guardian** syncs tracking and scores account health.

The agents also plan ahead. Collector books its own follow-up and final notice, Guardian books a carrier check, and Defender books a re-check 48 hours before PayPal's dispute deadline. The seller sees these on a timeline and can drag any of them. When one comes due it runs through the same gateway, so a plan that breaks a rule is blocked instead of run. When the facts change, for example the invoice gets paid, the agents cancel the plans that no longer make sense.

The console (React, AG Grid, Bryntum) shows money at risk, approvals, the ledger, the agents' timeline, disputes and invoices, with a one-click demo panel and a guided tour.

## How we built it
- PayPal sandbox, used live: Invoicing v2 (create, send, remind, record payment, record refund), Payments v2 capture refunds for invoices paid through PayPal, and Webhooks with `verify-webhook-signature` on every event (invoices paid and refunded, captures, disputes). The client uses OAuth with a cached token and sends a `PayPal-Request-Id` on every write, so a retry never acts twice.
- PayPal, built but replayed in the demo: Disputes (get, message, provide evidence, make offer, accept claim) and Shipment Tracking. The sandbox can't open a dispute on demand, so the demo's dispute and parcel are replayed from recorded PayPal payloads, and the ledger labels those calls "simulated".
- MCP: the official MCP Python SDK, streamable HTTP at `/mcp`, eight tools. Clients sign in with a signed 14-day link (for URL-only clients like ChatGPT) or HTTP Basic. Outside agents get their own identity in the gateway, with their own allowlist and caps.
- AI: one OpenAI-compatible wrapper with a fallback chain (Groq → Gemini → NVIDIA NIM). Agents return JSON validated against Pydantic schemas. Invalid output gets one retry, then the rules take over. Untrusted text such as emails and buyer messages is fenced and never followed as instructions. Rules decide anything that moves money; the model reads, flags, breaks ties and writes the words people read, and those words are checked before use.
- Evals on the real model, committed in `docs/evals/`: Sentinel 20/20 emails (0 scams missed, 0 false alarms), Defender 8/8 disputes (0 uncited facts, and all 8 AI-written notes passed the citation check), Collector 10/10 invoices, prompt injection 6/6 (every disallowed tool call denied).
- Backend: FastAPI and PostgreSQL, with an append-only ledger sealed under an advisory lock, a plan runner and signed session login. 75+ tests run in CI.
- Hosting: Render from `render.yaml`, with the database on Neon Postgres. Every push to `main` redeploys.

## Sponsor tools we built with
- Bryntum Scheduler is the agents' timeline. Each agent has a row, and the actions it has planned are dashed bars the seller can drag to a new time; the move is sealed in the ledger. Drop one on "now" and it runs within seconds through the gateway, and the bar turns ✓, ⏸ (waiting for approval) or ✕ (blocked, with the gateway's reason in the tooltip). Approvals, overdue invoices and PayPal's dispute deadline sit on the same schedule.
- AG Grid Community runs the Proof Ledger and Invoices tables. The ledger re-verifies the chain every few seconds. After a tamper, the broken record pins to the top in red and everything after it is marked unproven. A link column shows ✓ or ✕ per hash link, new records flash as they're sealed, a row click opens the full record, and the trail exports to CSV. Invoices flash when PayPal's webhook marks one paid or refunded, with an overdue bar and a pinned totals row.
- APIMatic: we cleaned up our OpenAPI spec against APIMatic's checks (SDK readiness 99/100, AI readiness 98/100) and generated the docs portal at https://aegisfleet.solvor.co.in/docs (live playground, code samples, an MCP page and `llms.txt`) plus Python, TypeScript and C# SDKs.
- Render hosts the app and the docs portal from one blueprint, with the PayPal sandbox and model keys in Render env vars.

## Challenges we ran into
- Making AI useful without trusting it. The rule we kept: AI drafts, classifies and recommends, and only the gateway's rules or a human approval execute a PayPal call.
- Letting outside agents in without opening a hole. They get their own identity in the gateway, a narrower allowlist, caps, and refunds bounded by the ledger's record of what the buyer actually paid.
- Free-tier rate limits during evals. The fallback chain absorbed them.
- Sandbox checkout failed for an India-region buyer account, so we kept a "record payment" path that fires the same signed webhook.

## Accomplishments that we're proud of
- An outside AI agent invoicing, getting paid and refunding on the real PayPal sandbox, with the seller approving the money move and PayPal's own signed webhooks confirming each step.
- Prompt-injected refunds are denied by the gateway's rules, which don't care how the prompt is worded.
- Every claim an agent makes about money points at a specific ledger entry, and the AI-written dispute note is thrown away if it doesn't.

## What we learned
Guardrails belong outside the model. A small gateway with allowlists, caps, human approval and a ledger made the agents easier to trust than any prompt could, and it let us open the door to agents we didn't write.

## What's next
- Put PayPal's own Agent Toolkit and MCP server behind the same gateway, so any PayPal tool an agent calls gets caps, approvals and a ledger.
- Per-seller limits and production mode, behind the same rules.
- Buyer-side agents: a shopper's agent requests a refund or pays an invoice through AegisFleet, and the seller's rules decide.

## Try it
- Live demo: https://aegisfleet.solvor.co.in (judge login is in the testing instructions)
- API docs and SDKs: https://aegisfleet.solvor.co.in/docs
- MCP endpoint: https://aegisfleet.solvor.co.in/mcp
- Code (MIT): https://github.com/Shivoo29/AegisFleet

---

## Built with
python, fastapi, postgresql, neon, mcp, react, typescript, vite, bryntum, ag-grid, apimatic, render, paypal-invoicing, paypal-payments, paypal-webhooks, paypal-disputes, groq, gemini, nvidia-nim

## Tools used (AI)
| Tool | Model | How we use it |
|---|---|---|
| Groq | `openai/gpt-oss-120b` | Primary model for all four agents: Sentinel's red flags, Defender's classification tie-breaks and its note to PayPal, Collector's reminder wording, Guardian's recommendations. JSON validated against Pydantic schemas. |
| Google Gemini API | `gemini-3.5-flash` | First fallback when Groq is rate-limited or errors. |
| NVIDIA NIM | `nemotron-3.5-super-vl-120b-a12b` | Second fallback. |
| Claude Code | – | Our coding assistant while building, and the outside agent we demo connecting over MCP. |

The models never call PayPal and never hold credentials. They return structured output; the gateway decides what runs.

## Testing instructions (judges only)
```
Live demo: https://aegisfleet.solvor.co.in
Log in with username judge and password <JUDGE_PASSWORD>

1. Open the Demo tab and click Reset demo state. A short guide then points at each step.
2. Click Real PayPal invoice to create a real sandbox invoice. Pay it with the sandbox buyer below, or click Record payment (backup). PayPal's signed webhook marks it paid on the Invoices tab within about a minute.
3. Click Overdue invoice, then open Timeline. Collector has booked a follow-up and a final notice. Drag the follow-up onto the red "now" line and it runs within a few seconds (✓). Drag the final notice there too and the gateway blocks it (✕), because the cap is 2 reminders a week.
4. Try Fake payment email, Replay injection and Tamper, then check Activity, Approvals and Ledger.
5. Optional, with your own AI: Demo → Connect any AI agent → Get my MCP link, then follow the steps for your client (ChatGPT, Claude, Gemini CLI, Cursor, VS Code or Codex). Ask it to invoice a buyer, pay the link it gives you (or click Record payment (backup)), then ask it to refund that invoice. Refunds of $100 or more wait for you in Approvals.

When you finish, please click Reset demo state again so the next judge starts clean.

Sandbox buyer for step 2: <BUYER_EMAIL> / <BUYER_PASSWORD>
Everything runs on the PayPal sandbox, and live mode is refused in code.
API docs and SDKs: https://aegisfleet.solvor.co.in/docs
Run it locally with no keys: SETUP.md in the repo.
```
