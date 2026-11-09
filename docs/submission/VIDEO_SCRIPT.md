# Demo video script (target 2:50, hard limit 3:00)

Record on https://aegisfleet.solvor.co.in, logged in as `dev`, browser at 1440×900, zoom 110%.
Screen recording + voice-over. No music (or royalty-free only). No PayPal logo on our own screens.

## Before you hit record
1. Incognito window A: AegisFleet, logged in. Guide already dismissed.
2. Incognito window B: sandbox.paypal.com, logged in as the **US** sandbox buyer.
3. In A: **Demo → Reset**. Wait for the result line. Header shows "Chain intact" and "1 awaiting approval".
4. Close every other tab and notification.

## Shot list

| Time | Screen | Do | Say |
|---|---|---|---|
| 0:00–0:15 | Overview | Slow pan over the stat cards | "Riya sells hand-made jewellery on PayPal. Three things cost sellers like her money: fake 'you got paid' emails, buyers who claim an order never arrived, and invoices nobody chases. AegisFleet puts AI agents on all three, without ever letting AI move money on its own." |
| 0:15–0:45 | Demo → **Real PayPal invoice** | Click. Click the PayPal link. Switch to window B, pay $600 | "This is a real PayPal sandbox invoice, issued through the Invoicing API from Riya's account. Her customer pays it with PayPal checkout." |
| 0:45–1:00 | Invoices | Switch back, wait for the row to flip to **paid** | "PayPal sends a signed webhook. We verify the signature with PayPal before trusting it, then seal the payment into our Proof Ledger. Now the invoice is paid, for real." |
| 1:00–1:30 | Demo → **Fake payment email**, then Activity | Click, open the Sentinel run | "Now a scammer emails: 'You received $600, ship the item now.' Sentinel, our first agent, doesn't trust the email. It checks the ledger for a verified PayPal payment, spots the lookalike domain, and flags it as a scam, in plain words the seller understands." |
| 1:30–2:05 | Disputes → PP-D-12345, then Approvals | Show checklist and facts, then click **Approve** | "A buyer opens an 'item not received' dispute. Defender pulls the sealed payment, tracking and delivery records and drafts the evidence. Every fact links to a ledger entry. But it can't send anything to PayPal itself: the gateway holds it until Riya approves." |
| 2:05–2:25 | Demo → **Replay injection** | Click, read the result line | "What if an email tricks an agent into refunding? Sentinel isn't allowed to call refunds. The gateway denies it and seals the attempt. AI drafts and recommends; only rules or a human move money." |
| 2:25–2:45 | Demo → **Tamper**, then header + Ledger | Click Tamper; header turns **Chain broken**; Ledger → Verify | "Every step is hash-chained. If anyone edits a past record, even directly in the database, verification points at the exact entry." |
| 2:45–2:55 | Overview | Hold | "AegisFleet. Get paid, stay paid. Live demo and code at the links below." |

## If something breaks while recording
- Sandbox checkout errors → **Record payment (backup)**: same signed webhook. Say "PayPal records the payment" instead of "her customer pays".
- Sentinel slow → cut the wait in editing.
- Anything else → Demo → Reset and re-take that shot only.

## Edit
- Cut dead time between clicks; keep each result on screen ≥ 2 s.
- Captions for the 5 key lines (judges often watch muted).
- Export 1080p, upload to YouTube as **Public**, paste the link in Devpost.
