from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from ...services.auth import AuthService
from ...services.partner_link import PartnerLinkService
from ...storage import get_store

router = APIRouter(prefix="/partners", tags=["partners"])


class InviteResponse(BaseModel):
    token: str
    status: str


@router.post("/invite", response_model=InviteResponse)
async def invite_partner(authorization: str | None = Header(default=None), store=Depends(get_store)):
    auth = AuthService(store)
    user = await auth.me(authorization.replace("Bearer ", "") if authorization else None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    svc = PartnerLinkService(store)
    rec = await svc.invite(user.id)
    return InviteResponse(token=rec.token or "", status=rec.status)


class AcceptRequest(BaseModel):
    token: str


@router.post("/accept")
async def accept_invite(payload: AcceptRequest, authorization: str | None = Header(default=None), store=Depends(get_store)) -> dict:
    auth = AuthService(store)
    user = await auth.me(authorization.replace("Bearer ", "") if authorization else None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    svc = PartnerLinkService(store)
    rec = await svc.accept(payload.token, user.id)
    if not rec:
        raise HTTPException(status_code=400, detail="Invalid or used token")
    return {"status": rec.status, "partner_user_id": rec.partner_user_id}


@router.get("/status")
async def partner_status(authorization: str | None = Header(default=None), store=Depends(get_store)) -> dict:
    auth = AuthService(store)
    user = await auth.me(authorization.replace("Bearer ", "") if authorization else None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    svc = PartnerLinkService(store)
    rec = await svc.status(user.id)
    if not rec:
        return {"status": "none"}
    # resolve partner name if possible
    partner_id = rec.partner_user_id if rec.user_id == user.id else rec.user_id
    partner_name = None
    if partner_id:
        partner = next((u for u in store.users if u.id == partner_id), None)
        partner_name = partner.name if partner else None
    return {
        "status": rec.status,
        "token": rec.token,
        "partner_user_id": partner_id,
        "partner_name": partner_name,
        "self_user_id": user.id,
        "self_name": user.name,
    }
