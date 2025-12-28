from __future__ import annotations

import secrets

from ..storage import InMemoryStore, PartnerLinkRecord


class PartnerLinkService:
    def __init__(self, store: InMemoryStore):
        self.store = store

    async def invite(self, user_id: str) -> PartnerLinkRecord:
        token = secrets.token_hex(12)
        return self.store.create_partner_link(user_id, token)

    async def accept(self, token: str, partner_user_id: str) -> PartnerLinkRecord | None:
        return self.store.accept_partner_link(token, partner_user_id)

    async def status(self, user_id: str) -> PartnerLinkRecord | None:
        return self.store.partner_status(user_id)
