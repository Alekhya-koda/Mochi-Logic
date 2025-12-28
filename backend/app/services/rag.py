from __future__ import annotations

from typing import Any


class RAGService:
    def __init__(self):
        pass

    async def retrieve(self, query: str) -> list[dict[str, Any]]:
        # Placeholder retrieval; production would query pgvector index of curated corpus
        return []
