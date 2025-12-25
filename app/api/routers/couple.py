from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException

from ...services.auth import AuthService
from ...storage import get_store

router = APIRouter(prefix="/couple", tags=["couple"])


@router.get("/summary")
async def couple_summary(authorization: str | None = Header(default=None), store=Depends(get_store)) -> dict:
    auth = AuthService(store)
    user = await auth.me(authorization.replace("Bearer ", "") if authorization else None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    partner_id = store.linked_partner_id(user.id)
    if not partner_id:
        return {"status": "unlinked"}

    # get latest conversation for both
    def latest_conv(uid: str):
        for conv in reversed(list(store.conversations.values())):
            if conv.user_id == uid:
                return conv
        return None

    user_conv = latest_conv(user.id)
    partner_conv = latest_conv(partner_id)

    def last_messages(conv_id: str | None, label: str):
        if not conv_id:
            return []
        msgs = store.list_messages(conv_id, limit=3)
        return [f"{label}: {m.content}" for m in msgs]

    combined = last_messages(user_conv.id if user_conv else None, "You") + last_messages(partner_conv.id if partner_conv else None, "Partner")
    summary_text = " | ".join(combined) if combined else "No shared history yet."

    partner = next((u for u in store.users if u.id == partner_id), None)
    you = user.name or "You"
    return {"status": "linked", "partner_name": partner.name if partner else None, "self_name": you, "summary": summary_text}
