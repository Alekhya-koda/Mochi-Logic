from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/risk-events", tags=["risk-events"])


@router.get("")
async def list_risk_events() -> dict:
    # Admin-protected listing stub
    return {"events": []}
