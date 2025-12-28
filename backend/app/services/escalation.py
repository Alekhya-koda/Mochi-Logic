from __future__ import annotations

from datetime import datetime
from typing import Sequence

from ..storage import InMemoryStore, Session


class EscalationService:
    def __init__(self, store: InMemoryStore):
        self.store = store

    async def prepare_session(self, participants: Sequence[str], allowed_context_ids: Sequence[str]) -> Session:
        return self.store.create_session(list(participants), list(allowed_context_ids))

    async def get_session(self, session_id: str) -> Session | None:
        return self.store.get_session(session_id)
