from __future__ import annotations

from ..storage import InMemoryStore, PartnerInsight, Summary
from .consent import ConsentService


class InsightsService:
    def __init__(self, store: InMemoryStore):
        self.store = store
        self.consent_service = ConsentService(store)

    async def list_for_viewer(self, viewer_id: str) -> list[PartnerInsight]:
        return self.store.list_insights(viewer_id)

    async def create_from_summary(
        self,
        summary: Summary,
        viewer_partner_id: str,
        scope: str = "summary.share",
    ) -> PartnerInsight | None:
        allowed = await self.consent_service.is_granted(
            user_id=summary.user_id,
            scope=scope,
            target_partner_id=viewer_partner_id,
        )
        if not allowed:
            return None
        return self.store.add_partner_insight(summary, viewer_partner_id)
