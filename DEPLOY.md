# Deploy: college server + Cloudflare Tunnel → https://aegisfleet.solvor.co.in

The server never opens a port. `cloudflared` dials **out** to Cloudflare, and Cloudflare
serves HTTPS on our domain. That works behind a college firewall/NAT, and PayPal webhooks get
the HTTPS URL they need.

```
browser / PayPal ──HTTPS──▶ Cloudflare ◀──outbound tunnel── cloudflared ─▶ app:8000 ─▶ db
```

## 1. Create the tunnel (Cloudflare dashboard, one time)

1. https://one.dash.cloudflare.com → **Networks → Tunnels → Create a tunnel** → **Cloudflared**.
2. Name: `aegisfleet` → Save.
3. Copy the **token** from the install command shown (the long string after `--token`).
   Don't run that command — Docker runs cloudflared for us.
4. **Public hostname** tab → Add:
   - Subdomain `aegisfleet`, domain `solvor.co.in`
   - Service: **HTTP**, URL **`app:8000`**
5. Save. Cloudflare creates the DNS record itself.

## 2. Server (one time)

Needs Docker + Docker Compose + git.

```bash
git clone https://github.com/Shivoo29/AegisFleet.git && cd AegisFleet
cp .env.example .env
nano .env
```

Server `.env` — differences from a laptop:

```
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=<sandbox client id>
PAYPAL_CLIENT_SECRET=<sandbox secret>
PAYPAL_WEBHOOK_ID=                      # fill after step 4
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-120b
LLM_FALLBACKS=gemini:gemini-3.5-flash,nvidia:nvidia/nemotron-3.5-super-vl-120b-a12b
GROQ_API_KEY=... GEMINI_API_KEY=... NVIDIA_API_KEY=...
CONSOLE_PASSWORD=<long random — app refuses "dev" outside fake mode>
POSTGRES_PASSWORD=<long random>
CLOUDFLARE_TUNNEL_TOKEN=<token from step 1>
```
`DATABASE_URL` is ignored here; compose points the app at the `db` container.
Random values: `openssl rand -base64 24`.

```bash
chmod 600 .env
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml logs -f    # Ctrl+C to stop watching
```

## 3. Check

- https://aegisfleet.solvor.co.in/healthz → `{"ok":true}`
- https://aegisfleet.solvor.co.in → console asks for password.

## 4. PayPal webhook

1. developer.paypal.com → Apps & Credentials → **Default Application** → **Webhooks → Add Webhook**.
2. URL: `https://aegisfleet.solvor.co.in/webhooks/paypal`
3. Events: Payment capture completed, Payment capture refunded, Invoice paid,
   Customer dispute created / updated / resolved.
4. Copy the **Webhook ID** into server `.env` → `PAYPAL_WEBHOOK_ID=`, then:
   `docker compose -f docker-compose.prod.yml up -d`

## Update after a push to main

```bash
cd AegisFleet && git pull
docker compose -f docker-compose.prod.yml up -d --build
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| Tunnel logs `failed to dial` / QUIC errors | College blocks UDP 7844. Add `--protocol http2` to the tunnel `command` in `docker-compose.prod.yml` |
| 502 / Bad gateway | App not up: `docker compose -f docker-compose.prod.yml logs app` |
| App exits "console password" | Set a real `CONSOLE_PASSWORD` |
| Wipe demo data | Console demo panel → Reset (or `POST /api/demo/reset`) |
