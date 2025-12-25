from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ...audit.logger import AuditLogger
from ...services.conversation import ConversationService
from ...services.llm_orchestrator import LLMOrchestrator
from ...services.rag import RAGService
from ...storage import get_store

router = APIRouter(prefix="/messages", tags=["messages"])


class MessageRequest(BaseModel):
    conversation_id: UUID
    user_id: UUID
    content: str = Field(..., max_length=4000)


class MessageResponse(BaseModel):
    user_message_id: UUID
    assistant_message_id: UUID
    assistant_summary_id: UUID | None
    content: str


@router.post("", response_model=MessageResponse)
async def post_message(payload: MessageRequest, store=Depends(get_store)):
    convo_service = ConversationService(store)
    rag_service = RAGService()
    llm = LLMOrchestrator()
    audit = AuditLogger(store)

    user_msg = await convo_service.post_message(
        str(payload.conversation_id),
        author_type="user",
        content=payload.content,
    )

    history = await convo_service.list_messages(str(payload.conversation_id), limit=5)
    context = [{"role": "assistant" if m.author_type == "assistant" else "user", "content": m.content} for m in history]

    # Pull partner context if linked (limited messages)
    partner_context = []
    link = store.partner_status(str(payload.user_id))
    if link and link.status == "linked":
        partner_id = link.partner_user_id if link.user_id == str(payload.user_id) else link.user_id
        partner_conv = store.latest_conversation_for_user(partner_id) if partner_id else None
        if partner_conv:
            partner_msgs = store.list_messages(partner_conv.id, limit=5)
            for pm in partner_msgs:
                partner_context.append({"role": "user", "content": f"[Partner] {pm.content}"})
    context.extend(partner_context)

    retrieved = await rag_service.retrieve(payload.content)
    for item in retrieved:
        context.append({"role": "system", "content": item.get("content", "")})

    llm_result = await llm.respond(payload.content, context=context)
    assistant_content = llm_result["content"]

    assistant_msg = await convo_service.post_message(
        str(payload.conversation_id),
        author_type="assistant",
        content=assistant_content,
    )
    summary = await convo_service.save_summary(
        str(payload.conversation_id),
        user_id=str(payload.user_id),
        summary_text=assistant_content,
        themes=[],
        confidence=50,
    )

    await audit.log(
        actor=str(payload.user_id),
        action="message.post",
        payload_meta={"conversation_id": str(payload.conversation_id)},
        risk_level="medium" if llm_result.get("issues") else "low",
    )

    return MessageResponse(
        user_message_id=user_msg.id,
        assistant_message_id=assistant_msg.id,
        assistant_summary_id=summary.id,
        content=assistant_content,
    )
