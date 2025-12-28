"""Lightweight local knowledge base for RAG over curated sources."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4

import numpy as np
from openai import AsyncOpenAI

EMBED_MODEL = "text-embedding-3-small"
DEFAULT_DB_PATH = Path(__file__).resolve().parent / "data" / "knowledge_base.jsonl"


@dataclass
class KnowledgeRecord:
    """Single chunk stored in the knowledge base."""

    id: str
    url: str
    title: str | None
    text: str
    embedding: list[float]
    source_type: str | None = None
    chunk_index: int | None = None


@dataclass
class KnowledgeResult:
    """Chunk returned from a similarity search."""

    record: KnowledgeRecord
    score: float


class KnowledgeBase:
    """Minimal vector store for running cosine similarity searches locally."""

    def __init__(
        self,
        db_path: Path | str = DEFAULT_DB_PATH,
        embed_model: str = EMBED_MODEL,
        client: AsyncOpenAI | None = None,
    ) -> None:
        self.db_path = Path(db_path)
        self.embed_model = embed_model
        self.client = client or AsyncOpenAI()
        self._records: list[KnowledgeRecord] | None = None
        self._matrix: np.ndarray | None = None

    def ensure_loaded(self) -> None:
        """Load records and embed matrix from disk if not already cached."""
        if self._records is not None and self._matrix is not None:
            return
        self._records = []
        self._matrix = np.zeros((0, 0), dtype=np.float32)

        if not self.db_path.exists():
            return

        records: list[KnowledgeRecord] = []
        vectors: list[list[float]] = []
        with self.db_path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    record = KnowledgeRecord(
                        id=row.get("id", str(uuid4())),
                        url=row.get("url", "unknown"),
                        title=row.get("title"),
                        text=row.get("text", ""),
                        embedding=row.get("embedding") or [],
                        source_type=row.get("source_type"),
                        chunk_index=row.get("chunk_index"),
                    )
                except (json.JSONDecodeError, TypeError):
                    continue
                if not record.embedding or not record.text:
                    continue
                records.append(record)
                vectors.append(record.embedding)

        if not records:
            return

        self._records = records
        matrix = np.array(vectors, dtype=np.float32)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self._matrix = matrix / norms

    async def search(self, query: str, top_k: int = 5) -> list[KnowledgeResult]:
        """Embed the query and return the closest chunks."""
        if top_k <= 0:
            return []

        self.ensure_loaded()
        if not self._records or self._matrix is None or not len(self._matrix):
            return []

        query_embedding = await self._embed_text(query)
        if not query_embedding:
            return []

        query_vector = np.array([query_embedding], dtype=np.float32)
        query_norm = np.linalg.norm(query_vector, axis=1, keepdims=True)
        query_norm[query_norm == 0] = 1.0
        query_vector = query_vector / query_norm

        scores = self._matrix.dot(query_vector.T).reshape(-1)
        top_indices = np.argsort(scores)[::-1][:top_k]

        results: list[KnowledgeResult] = []
        for idx in top_indices:
            score = float(scores[idx])
            record = self._records[idx]
            # Filter out extremely low matches to avoid noise.
            if math.isnan(score):
                continue
            results.append(KnowledgeResult(record=record, score=score))
        return results

    async def _embed_text(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.embed_model, input=text
        )
        return response.data[0].embedding


def build_snippet(text: str, max_chars: int = 500) -> str:
    """Return a compact snippet for tool responses."""
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."
