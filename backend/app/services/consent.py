from __future__ import annotations

from typing import Sequence

from ..storage import Consent, InMemoryStore


class ConsentService:
    def __init__(self, store: InMemoryStore):
        self.store = store

    async def grant(self, user_id: str, scope: str, target_partner_id: str | None = None) -> Consent:
        return self.store.grant_consent(user_id, scope, target_partner_id)

    async def revoke(self, user_id: str, scope: str, target_partner_id: str | None = None) -> Consent:
        return self.store.revoke_consent(user_id, scope, target_partner_id)

    async def list_active(self, user_id: str, scope_prefix: str | None = None) -> Sequence[Consent]:
        consents = self.store.list_consents(user_id)
        if scope_prefix:
            consents = [c for c in consents if c.scope.startswith(scope_prefix)]
        return consents

    async def is_granted(self, user_id: str, scope: str, target_partner_id: str | None = None) -> bool:
        return self.store.is_consent_granted(user_id, scope, target_partner_id)
