from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/partners", tags=["partners"])


class InviteRequest(BaseModel):
    email: str


@router.post("/invite")
async def invite_partner(_: InviteRequest) -> dict:
    return {"status": "sent"}


@router.post("/accept")
async def accept_invite(token: str) -> dict:
    return {"status": "accepted", "token": token}


@router.get("/status")
async def partner_status() -> dict:
    return {"status": "pending"}
