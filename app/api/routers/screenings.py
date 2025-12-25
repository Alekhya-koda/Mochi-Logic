from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...services.screening import ScreeningService
from ...storage import get_store

router = APIRouter(prefix="/screenings", tags=["screenings"])


class ScreeningRequest(BaseModel):
    user_id: UUID
    instrument: str
    answers: dict


@router.post("")
async def submit_screening(payload: ScreeningRequest, store=Depends(get_store)) -> dict:
    service = ScreeningService(store)
    screening = await service.submit(str(payload.user_id), payload.instrument, payload.answers)
    history = await service.list_history(str(payload.user_id), limit=5)
    trend = await service.update_trend(str(payload.user_id), history)
    if "trend_up" in trend.flags:
        await service.log_risk_event(str(payload.user_id), level="medium", reason_codes=trend.flags)
    return {"id": screening.id, "trend": {"status": trend.status, "flags": trend.flags}}


@router.get("/history")
async def screening_history(user_id: UUID, store=Depends(get_store)) -> dict:
    service = ScreeningService(store)
    screenings = await service.list_history(str(user_id))
    return {
        "screenings": [
            {"id": s.id, "instrument": s.instrument, "score_meta": s.score_meta, "created_at": s.created_at}
            for s in screenings
        ]
    }
