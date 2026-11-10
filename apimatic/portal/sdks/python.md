# Python SDK (/docs/sdks/python)

[Download SDK](/docs/__downloads/sdk/python.zip)

## Intro [#intro]

The AegisFleet SDK provides access to the AegisFleet REST APIs.

Seller console API for AegisFleet: AI agents that guard a PayPal seller's payments, disputes, invoices and shipments. Agents never call PayPal directly; every action passes a guardrail gateway (kill switch, allowlist, caps, human approval) and is sealed into a hash-chained Proof Ledger.

Authenticate with HTTP Basic (`dev` or `judge`) or the session cookie set by `POST /api/login`.

## Installation [#installation]

Add the SDK to your project from its folder, with whichever package manager your project uses. Give each tool a path containing a slash, such as `../aegis-fleet` — a bare folder name is looked up on PyPI instead, and resolves to whatever project holds that name there:

```bash
pip install <path-to-sdk>
```

```bash
uv add <path-to-sdk>
```

```bash
poetry add <path-to-sdk>
```

## Quick Start [#quick-start]

### Synchronous client [#synchronous-client]

Construct `AegisFleetClient` with keyword arguments, and call `close()` when you are done. Every argument is optional.

```python
from aegis_fleet import AegisFleetClient
from aegis_fleet.core import BasicAuthCredentials

client = AegisFleetClient(http_basic=BasicAuthCredentials(username="YOUR_USERNAME", password="YOUR_PASSWORD"))

client.close()
```

Alternatively, scope it — `with AegisFleetClient(...) as client:` closes the pool on exit.

### Asynchronous client [#asynchronous-client]

`AsyncAegisFleetClient` mirrors `AegisFleetClient` with **identical method names**, and every endpoint method is a coroutine. It takes the same arguments, with some differences — for example, the transport argument is `custom_async_http_client`.

```python
from asyncio import run

from aegis_fleet import AsyncAegisFleetClient
from aegis_fleet.core import BasicAuthCredentials

async def main() -> None:
    client = AsyncAegisFleetClient(http_basic=BasicAuthCredentials(username="YOUR_USERNAME", password="YOUR_PASSWORD"))
    await client.aclose()

run(main())
```

Alternatively, scope it — `async with AsyncAegisFleetClient(...) as client:` closes the pool on exit.