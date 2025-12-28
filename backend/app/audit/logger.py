from __future__ import annotations

from datetime import datetime
from typing import Any

from ..storage import AuditLog, InMemoryStore


class AuditLogger:
    def __init__(self, store: InMemoryStore):
        self.store = store

    async def log(self, actor: str, action: str, payload_meta: dict[str, Any], risk_level: str = "low") -> AuditLog:
        return self.store.add_audit(actor=actor, action=action, payload_meta=payload_meta, risk_level=risk_level)
