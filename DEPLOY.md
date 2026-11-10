# Deploy: Render

Live at https://aegisfleet.solvor.co.in (a DNS-only CNAME to `aegisfleet.onrender.com`).

- `render.yaml` is the blueprint: one Docker web service (Singapore, free plan) built from `Dockerfile`, which
  bundles the FastAPI backend, the built React console and the APIMatic docs portal.
- Every push to `main` redeploys automatically.
- The database is Neon Postgres (Singapore, direct connection, not the pooler). Its connection string is set as
  `DATABASE_URL` in the Render dashboard; tables are created at startup.
- Secrets are set only in the Render dashboard, never in the repo: `CONSOLE_PASSWORD`, `JUDGE_PASSWORD`,
  `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_WEBHOOK_ID`, `GROQ_API_KEY`, `GEMINI_API_KEY`, `NVIDIA_API_KEY`.
- The PayPal sandbox webhook points at `https://aegisfleet.solvor.co.in/webhooks/paypal`.
- `.github/workflows/keepalive.yml` pings `/healthz` every 5 minutes so the free instance doesn't sleep.

After switching databases, open the console and run **Demo → Reset demo state**.
