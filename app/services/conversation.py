from __future__ import annotations

from typing import Sequence

from ..storage import InMemoryStore, Message, Summary


class ConversationService:
    def __init__(self, store: InMemoryStore):
        self.store = store

    async def create_conversation(self, user_id: str, conv_type: str = "private"):
        return self.store.create_conversation(user_id=user_id, conv_type=conv_type)

    async def post_message(self, conversation_id: str, author_type: str, content: str) -> Message:
        return self.store.add_message(conversation_id, author_type, content)

    async def list_messages(self, conversation_id: str, limit: int = 50) -> Sequence[Message]:
        return self.store.list_messages(conversation_id, limit)

    async def save_summary(
        self,
        conversation_id: str,
        user_id: str,
        summary_text: str,
        themes: list[str] | None = None,
        confidence: int = 0,
    ) -> Summary:
        return self.store.add_summary(conversation_id, user_id, summary_text, themes or [], confidence)
