# TypeScript SDK (/docs/sdks/typescript)

[Download SDK](/docs/__downloads/sdk/typescript.zip)

## Intro [#intro]

The AegisFleet SDK provides access to the AegisFleet REST APIs.

Seller console API for AegisFleet: AI agents that guard a PayPal seller's payments, disputes, invoices and shipments. Agents never call PayPal directly; every action passes a guardrail gateway (kill switch, allowlist, caps, human approval) and is sealed into a hash-chained Proof Ledger.

Authenticate with HTTP Basic (`dev` or `judge`) or the session cookie set by `POST /api/login`.

## Installation [#installation]

The SDK compiles to `dist/` before it can be referenced — run its `build` script once in the SDK folder, then add it to your project by path:

```bash
npm install <path-to-sdk>
```

## Quick Start [#quick-start]

Create one client and reuse it. Configure its behaviour through `ClientOptions`.

```ts
import { AegisFleetClient } from "aegis-fleet";

const client = new AegisFleetClient({
  httpBasic: { username: "YOUR_USERNAME", password: "YOUR_PASSWORD" },
});
```

Nothing in `ClientOptions` is required — `new AegisFleetClient()` compiles — and each option left out falls back to its default. This API declares one environment, so there is no environment to select and no host to state at the construction site.

### From CommonJS [#from-commonjs]

The package ships both dialects from a single entry, so `require` works with full types. In a TypeScript CommonJS file use the `import ... = require(...)` form — a plain destructuring `require` runs fine but gives you `any`.

```ts
import sdk = require("aegis-fleet");

const client = new sdk.AegisFleetClient({
  httpBasic: { username: "YOUR_USERNAME", password: "YOUR_PASSWORD" },
});
```