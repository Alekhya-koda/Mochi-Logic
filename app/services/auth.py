from __future__ import annotations

import hashlib
import secrets

from ..storage import InMemoryStore, User


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class AuthService:
    def __init__(self, store: InMemoryStore):
        self.store = store

    async def signup(self, email: str, password: str, name: str | None = None) -> tuple[User, str]:
        existing = self.store.find_user_by_email(email)
        if existing:
            raise ValueError("email_exists")
        user = self.store.add_user(email=email, password_hash=_hash_password(password), name=name)
        token = secrets.token_hex(16)
        self.store.store_token(token, user.id)
        return user, token

    async def login(self, email: str, password: str) -> tuple[User, str]:
        user = self.store.find_user_by_email(email)
        if not user or user.password_hash != _hash_password(password):
            raise ValueError("invalid_credentials")
        token = secrets.token_hex(16)
        self.store.store_token(token, user.id)
        return user, token

    async def me(self, token: str | None) -> User | None:
        if not token:
            return None
        return self.store.get_user_by_token(token)
