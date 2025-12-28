from __future__ import annotations

from typing import Any, Sequence

from ..storage import InMemoryStore, RiskEvent, Screening, ScreeningTrend


class ScreeningService:
    def __init__(self, store: InMemoryStore):
        self.store = store

    async def submit(self, user_id: str, instrument: str, answers: dict[str, Any]) -> Screening:
        score_meta = {"score": sum(int(v) for v in answers.values() if isinstance(v, (int, float)))}
        return self.store.add_screening(user_id, instrument, answers, score_meta)

    async def list_history(self, user_id: str, limit: int = 20) -> Sequence[Screening]:
        return self.store.list_screenings(user_id, limit)

    async def update_trend(self, user_id: str, screenings: Sequence[Screening]) -> ScreeningTrend:
        scores = [s.score_meta.get("score", 0) for s in screenings]
        status = "steady"
        flags: list[str] = []
        if len(scores) >= 3 and scores[-1] > scores[0] + 3:
            status = "rising"
            flags.append("trend_up")
        return self.store.add_trend(user_id, window="28d", status=status, flags=flags)

    async def log_risk_event(self, user_id: str, level: str, reason_codes: list[str]) -> RiskEvent:
        return self.store.add_risk_event(user_id, source="screening", level=level, reason_codes=reason_codes)
