from __future__ import annotations

from typing import Sequence

from ..storage import RiskEvent, ScreeningTrend
from .screening import ScreeningService


class RiskEngine:
    def __init__(self, screening_service: ScreeningService):
        self.screening_service = screening_service

    async def evaluate_trends(self, user_id: str, trends: Sequence[ScreeningTrend]) -> RiskEvent | None:
        latest = trends[-1] if trends else None
        if latest and "trend_up" in latest.flags:
            return await self.screening_service.log_risk_event(
                user_id=user_id,
                level="medium",
                reason_codes=["trend_up"],
            )
        return None
