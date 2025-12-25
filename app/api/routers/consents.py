from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...services.consent import ConsentService
from ...storage import get_store

router = APIRouter(prefix="/consents", tags=["consents"])


class ConsentRequest(BaseModel):
    scope: str
    target_partner_id: UUID | None = None
    user_id: UUID


@router.post("/grant")
async def grant_consent(payload: ConsentRequest, store=Depends(get_store)) -> dict:
    service = ConsentService(store)
    consent = await service.grant(str(payload.user_id), payload.scope, str(payload.target_partner_id) if payload.target_partner_id else None)
    return {"id": consent.id, "status": consent.status}


@router.post("/revoke")
async def revoke_consent(payload: ConsentRequest, store=Depends(get_store)) -> dict:
    service = ConsentService(store)
    consent = await service.revoke(str(payload.user_id), payload.scope, str(payload.target_partner_id) if payload.target_partner_id else None)
    return {"id": consent.id, "status": consent.status}


@router.get("")
async def list_consents(user_id: UUID, store=Depends(get_store)) -> dict:
    service = ConsentService(store)
    consents = await service.list_active(str(user_id))
    return {"consents": [{"id": c.id, "scope": c.scope, "status": c.status} for c in consents]}
