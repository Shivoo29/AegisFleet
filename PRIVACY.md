# Privacy policy

AegisFleet is a hackathon project that runs against the **PayPal sandbox only**. It processes no real payments
and no real customer data, and live PayPal mode is refused in code.

## What the service stores
- **Sandbox business data** (invoices, disputes, shipments, demo emails) in the project's own PostgreSQL
  database, so agents can act on it and the console can show it.
- **A ledger** of every agent action and gateway decision, including which MCP client and console user made it
  (for example `claude-code (dev)`), so every money move can be audited.
- **Session cookies and MCP tokens**, signed and time-limited, used only to log you in.

## What it does not do
- No analytics, tracking or advertising, and no selling or sharing of data.
- MCP clients reach PayPal only through the gateway. The PayPal and AI model credentials stay on the server and are never sent to clients.

## Third parties
- **PayPal (sandbox):** invoices, payments, refunds, disputes, webhooks.
- **AI providers (Groq, Google Gemini, NVIDIA NIM):** agents send fenced, sandbox-only text to classify or draft
  replies. No credentials are sent.
- **Render and Neon:** hosting and the database.

## Retention
The demo data can be wiped at any time with **Demo → Reset demo state**. The hackathon deployment will be shut down
after judging.

## Contact
Open an issue at https://github.com/Shivoo29/AegisFleet/issues.
