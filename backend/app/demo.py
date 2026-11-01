"""Demo endpoints (M8). Only active when DEMO_MODE=true."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.config import get_settings

router = APIRouter(prefix="/api/demo")


def _demo_only():
    if not get_settings().demo_mode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="demo mode disabled")


@router.get("/status", dependencies=[Depends(_demo_only)])
async def status() -> dict:
    return {"demo": True}


@router.post("/scam_email", dependencies=[Depends(_demo_only)])
async def scam_email() -> dict:
    # TODO(SKJ): seed a scam email event and route it.
    return {"ok": True}


@router.post("/delivered", dependencies=[Depends(_demo_only)])
async def delivered() -> dict:
    # TODO(SKJ): seed a delivery.confirmed event.
    return {"ok": True}


@router.post("/replay_injection", dependencies=[Depends(_demo_only)])
async def replay_injection() -> dict:
    # TODO(SKJ): replay create_refund from an agent → gateway DENY.
    return {"ok": True}


@router.post("/tamper", dependencies=[Depends(_demo_only)])
async def tamper() -> dict:
    # TODO(SKJ): tamper one ledger payload → verify() broken_at.
    return {"ok": True}


@router.post("/reset", dependencies=[Depends(_demo_only)])
async def reset() -> dict:
    # TODO(SKJ): truncate demo tables.
    return {"ok": True}