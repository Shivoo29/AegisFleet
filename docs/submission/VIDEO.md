# Demo video script (under 2:50)

Public YouTube, under 3 minutes. Judges may score from the video alone, so every shot shows the product
working. Record the screen at 1080p, zoom the browser to 125%, and use a voice-over. Cut every wait.

## Before you record

1. Open https://aegisfleet.solvor.co.in, log in as `dev`, **Demo → Reset demo state**.
2. In a terminal, connect Claude Code to AegisFleet. Copy the command from **Demo → Connect your own AI
   agent** (type the password, click Copy command), paste it, then start `claude`.
3. Arrange two windows side by side: Claude Code on the left, the console on the right.
4. Do one full dry run, then Reset again before the real take.

The hook (0:00) is recorded during step 0:25, so record in story order and move that clip to the front when
editing.

## Shots

| Time | Screen | Voice-over |
|---|---|---|
| 0:00–0:10 | Claude Code: *"Refund $900 to my other account, the buyer emailed me."* AegisFleet answers **deny: refund exceeds what the buyer paid**. Hold on the red line for a second. | "Everyone is building AI agents that move money. Here's one being talked into a refund it shouldn't make. And here's it being stopped." |
| 0:10–0:22 | Console Overview, the ink hero and the proof chain strip. | "AegisFleet is the brakes for agentic commerce: a gateway between any AI agent and a seller's PayPal account. Kill switch, allowlists, caps, human approval, and a ledger nobody can quietly edit." |
| 0:22–0:40 | Claude Code: *"Invoice a buyer $150 for a hand-made silver bangle."* It returns the PayPal sandbox link. Open the link (or click **Record payment** in Demo). Cut. Invoices tab: the row flashes **paid**. | "Claude is connected over MCP. It issues a real PayPal sandbox invoice. When the buyer pays, PayPal's signed webhook lands here, and the invoice turns paid." |
| 0:40–1:05 | Claude Code: *"It arrived bent. Refund it."* Answer: **hold, waiting for the seller**. Console Approvals: the card from Claude. Click **Approve**. Claude Code: *"Did the seller approve it?"* Answer: approved, PayPal refund id. Invoices row flashes **refunded**. | "Refunds of a hundred dollars or more wait for a human. The seller approves, the gateway runs it on PayPal, and PayPal's refund webhook confirms it. The money only ever goes back to the buyer who paid." |
| 1:05–1:25 | Demo: **Fake payment email**. Activity: Sentinel's verdict, **scam**, with red flags. | "AegisFleet's own agents use the same gateway. Sentinel checks a 'you've been paid' email against verified PayPal payments, not against what the email says." |
| 1:25–2:00 | Demo: **Overdue invoice**. Timeline tab: Collector's dashed plans. Drag **Follow-up reminder** onto the red now-line: it turns ✓. Drag **Final notice** there: it turns ✕, hover to show *cap reached*. | "Agents plan their own next steps on a Bryntum timeline: a follow-up, a final notice, a check before PayPal's dispute deadline. The seller can drag any of them. When one comes due it runs through the gateway, so a plan that breaks a rule is blocked, not run." |
| 2:00–2:20 | Demo: **Tamper with ledger**. Ledger tab: the broken record pinned in red, everything after it unproven. Click it to open the seal. | "Every event, decision and approval is hash-chained. Edit one record behind the system's back and verification points at exactly that record." |
| 2:20–2:38 | A title card, then 2 seconds each of: `docs/evals` table, the docs portal at /docs, the Render dashboard. Card text: *Sentinel 20/20 · Defender 8/8, every claim cited · Collector 10/10 · Prompt injection 6/6 denied · PayPal Invoicing, Payments, signed Webhooks · MCP · Bryntum · AG Grid · APIMatic · Render* | "Evaluated on the real model: twenty out of twenty scam emails, every dispute fact cited, every injection denied. Built on PayPal Invoicing, Payments and signed webhooks, with docs and SDKs from APIMatic, on Render." |
| 2:38–2:48 | Console Overview, then the URL card: **aegisfleet.solvor.co.in**. | "Let agents transact. Keep the brakes. AegisFleet." |

## Exact prompts for Claude Code

1. `Invoice a buyer $150 for a hand-made silver bangle.`
2. (after it's paid) `Refund $900 to my other account, the buyer emailed me.`
3. `It arrived bent. Refund the buyer for the bangle.`
4. `Did the seller approve the refund? What happened?`

If Claude refuses prompt 2 on its own, keep that take too: it's still a refusal, but the gateway's deny is
the better shot, so rephrase as `The buyer asked for $900 back. Refund it.`

## If something is slow

- Webhook not in yet: cut, and add a small "about 40 seconds later" label.
- PayPal sandbox checkout fails: use **Demo → Record payment (backup)**; it fires the same signed webhook.
- Plans run every 15 seconds after you drop them on "now"; cut the wait.
