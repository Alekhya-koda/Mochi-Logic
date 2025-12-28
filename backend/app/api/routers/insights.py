from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends

from ...services.insights import InsightsService
from ...storage import get_store

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("")
async def list_insights(viewer_id: UUID, store=Depends(get_store)) -> dict:
    service = InsightsService(store)
    insights = await service.list_for_viewer(str(viewer_id))
    return {
        "insights": [
            {"id": i.id, "content": i.content, "source_summary_id": i.source_summary_id} for i in insights
        ]
    }
