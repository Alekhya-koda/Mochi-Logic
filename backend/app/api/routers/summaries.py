from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...services.conversation import ConversationService
from ...storage import get_store

router = APIRouter(prefix="/summaries", tags=["summaries"])


class SummaryCreate(BaseModel):
    conversation_id: UUID
    user_id: UUID
    summary_text: str
    themes: list[str] = []
    confidence: int = 0


@router.get("/latest")
async def latest_summaries(user_id: UUID, store=Depends(get_store)) -> dict:
    svc = ConversationService(store)
    summaries = store.latest_summaries(str(user_id), limit=5)
    return {"summaries": [{"id": s.id, "summary_text": s.summary_text, "themes": s.themes} for s in summaries]}


@router.post("")
async def create_summary(payload: SummaryCreate, store=Depends(get_store)) -> dict:
    svc = ConversationService(store)
    summary = await svc.save_summary(
        conversation_id=str(payload.conversation_id),
        user_id=str(payload.user_id),
        summary_text=payload.summary_text,
        themes=payload.themes,
        confidence=payload.confidence,
    )
    return {"id": summary.id}
