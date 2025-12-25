from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...services.escalation import EscalationService
from ...storage import get_store

router = APIRouter(prefix="/escalations", tags=["escalations"])


class PrepareEscalation(BaseModel):
    participants: list[UUID]
    allowed_context_ids: list[UUID]


@router.post("/prepare")
async def prepare(payload: PrepareEscalation, store=Depends(get_store)) -> dict:
    svc = EscalationService(store)
    session_obj = await svc.prepare_session(
        participants=[str(p) for p in payload.participants],
        allowed_context_ids=[str(cid) for cid in payload.allowed_context_ids],
    )
    return {"id": session_obj.id, "status": session_obj.status}


@router.get("/{session_id}")
async def get_session(session_id: UUID, store=Depends(get_store)) -> dict:
    svc = EscalationService(store)
    session_obj = await svc.get_session(str(session_id))
    if not session_obj:
        return {"error": "not_found"}
    return {
        "id": session_obj.id,
        "status": session_obj.status,
        "participants": session_obj.participants,
        "allowed_context_ids": session_obj.allowed_context_ids,
    }
