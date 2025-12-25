from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str


@router.post("/login", response_model=LoginResponse)
async def login(_: LoginRequest) -> LoginResponse:
    # Stub login flow
    return LoginResponse(token="stub-token")


@router.post("/logout")
async def logout() -> dict:
    return {"status": "ok"}


@router.get("/me")
async def me() -> dict:
    return {"user": {"id": "stub", "email": "user@example.com"}}
