from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel, EmailStr

from ...services.auth import AuthService
from ...storage import get_store

router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
async def signup(payload: SignupRequest, store=Depends(get_store)) -> dict:
    service = AuthService(store)
    try:
        user, token = await service.signup(payload.email, payload.password, payload.name)
    except ValueError as e:
        if str(e) == "email_exists":
            raise HTTPException(status_code=400, detail="Email already registered")
        raise
    return {"user_id": user.id, "token": token}


@router.post("/login")
async def login(payload: LoginRequest, store=Depends(get_store)) -> dict:
    service = AuthService(store)
    try:
        user, token = await service.login(payload.email, payload.password)
    except ValueError as e:
        if str(e) == "invalid_credentials":
            raise HTTPException(status_code=401, detail="Invalid credentials")
        raise
    return {"user_id": user.id, "token": token}


@router.get("/me")
async def me(authorization: str | None = Header(default=None), store=Depends(get_store)) -> dict:
    token = authorization.replace("Bearer ", "") if authorization else None
    service = AuthService(store)
    user = await service.me(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"user_id": user.id, "email": user.email}
