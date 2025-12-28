from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...services.conversation import ConversationService
from ...storage import get_store

router = APIRouter(prefix="/conversations", tags=["conversations"])


class ConversationCreate(BaseModel):
    user_id: UUID
    type: str = "private"


class ConversationResponse(BaseModel):
    id: UUID
    status: str


@router.post("", response_model=ConversationResponse)
async def create_conversation(payload: ConversationCreate, store=Depends(get_store)):
    svc = ConversationService(store)
    convo = await svc.create_conversation(str(payload.user_id), conv_type=payload.type)
    return ConversationResponse(id=convo.id, status=convo.status)


@router.get("/{conversation_id}/messages")
async def fetch_history(conversation_id: UUID, store=Depends(get_store)) -> dict:
    svc = ConversationService(store)
    messages = await svc.list_messages(str(conversation_id))
    return {"messages": [{"id": m.id, "content": m.content, "author_type": m.author_type} for m in messages]}
