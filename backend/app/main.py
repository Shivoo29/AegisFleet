"""FastAPI app (M8/M18)."""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.routing import Route

from app.api import router as api_router
from app.demo import router as demo_router
from app.paypal.webhooks import router as webhook_router
from app.db import init_schema
from app import mcp_server


@asynccontextmanager
async def _lifespan(_app):
    init_schema()  # fail loudly if DB is down
    async with mcp_server.running():
        yield


app = FastAPI(
    lifespan=_lifespan,
    docs_url="/swagger",  # /docs is the APIMatic portal
    generate_unique_id_function=lambda r: r.name,  # operationIds become SDK method names
    title="AegisFleet",
    version="1.0.0",
    description=(
        "Seller console API for AegisFleet: AI agents that guard a PayPal seller's payments, disputes, "
        "invoices and shipments. Agents never call PayPal directly; every action passes a guardrail "
        "gateway (kill switch, allowlist, caps, human approval) and is sealed into a hash-chained Proof Ledger.\n\n"
        "Authenticate with HTTP Basic (`dev` or `judge`) or the session cookie set by `POST /api/login`."
    ),
    servers=[{"url": "https://aegisfleet.solvor.co.in", "description": "Live demo (PayPal sandbox)"}],
    openapi_tags=[
        {"name": "console", "description": "Summary, Proof Ledger, approvals, agent runs, disputes, invoices, health."},
        {"name": "demo", "description": "One-click story beats for judges (demo mode only)."},
        {"name": "ops", "description": "Liveness probe."},
        {"name": "webhooks", "description": "PayPal webhook receiver; signatures are verified with PayPal before routing."},
    ],
)


def _openapi() -> dict:
    if not app.openapi_schema:
        from fastapi.openapi.utils import get_openapi
        from app.openapi_polish import polish
        app.openapi_schema = polish(get_openapi(title=app.title, version=app.version, description=app.description,
                                                routes=app.routes, servers=app.servers, tags=app.openapi_tags))
    return app.openapi_schema


app.openapi = _openapi
app.include_router(api_router)
app.include_router(demo_router)
app.include_router(webhook_router)


@app.get("/healthz")
async def healthz() -> dict:
    """Liveness probe for Render and the keep-alive ping. No auth."""
    return {"ok": True}


# MCP endpoint for outside AI agents (not in the OpenAPI spec; it speaks JSON-RPC).
app.router.routes.append(Route("/mcp", endpoint=mcp_server.endpoint, methods=["GET", "POST", "DELETE"]))

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_portal = os.path.join(_root, "apimatic", "portal")


@app.get("/docs", include_in_schema=False)
def _docs_slash() -> RedirectResponse:
    return RedirectResponse("/docs/")


if os.path.isdir(_portal):  # APIMatic docs portal: `apimatic portal generate` in apimatic/
    app.mount("/docs", StaticFiles(directory=_portal, html=True), name="docs")

# Serve frontend/dist if it exists (after API routes).
_frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "dist")
if os.path.isdir(_frontend_dist):
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="frontend")