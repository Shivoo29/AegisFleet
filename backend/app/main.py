"""FastAPI app (M8/M18)."""
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import router as api_router
from app.demo import router as demo_router
from app.paypal.webhooks import router as webhook_router
from app.db import init_schema

app = FastAPI(title="AegisFleet", version="0.1.0")


@app.on_event("startup")
def _startup() -> None:
    init_schema()  # fail loudly if DB is down


app.include_router(api_router)
app.include_router(demo_router)
app.include_router(webhook_router)


@app.get("/healthz")
async def healthz() -> dict:
    return {"ok": True}


# Serve frontend/dist if it exists (after API routes).
_frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "dist")
if os.path.isdir(_frontend_dist):
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="frontend")