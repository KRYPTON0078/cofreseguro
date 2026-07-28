"""Auth routes with password policy, lockout, and refresh tokens."""

from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select

from cofreseguro.auth.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)
from cofreseguro.shared.config import get_settings
from cofreseguro.shared.database import get_session_factory
from cofreseguro.shared.metrics import LOGIN_TOTAL
from cofreseguro.shared.models import RefreshToken, User

router = APIRouter(prefix="/v1/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = ""
    locale: str = "en"


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class RefreshIn(BaseModel):
    refresh_token: str


class ChangePasswordIn(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


def _password_ok(password: str) -> bool:
    if len(password) < 8:
        return False
    classes = sum(
        [
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(not c.isalnum() for c in password),
        ]
    )
    return classes >= 2


def _hash_refresh(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


async def _issue_refresh(user_id: int) -> str:
    raw = secrets.token_urlsafe(32)
    factory = get_session_factory()
    async with factory() as session:
        session.add(RefreshToken(user_id=user_id, token_hash=_hash_refresh(raw)))
        await session.commit()
    return raw


async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(security),
) -> User:
    if creds is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    try:
        payload = decode_token(creds.credentials)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from exc
    factory = get_session_factory()
    async with factory() as session:
        user = (
            await session.execute(select(User).where(User.email == payload.sub))
        ).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    return user


@router.post("/register", response_model=TokenOut)
async def register(body: RegisterIn) -> TokenOut:
    if not _password_ok(body.password):
        raise HTTPException(status_code=400, detail="password too weak")
    factory = get_session_factory()
    async with factory() as session:
        existing = (
            await session.execute(select(User).where(User.email == body.email.lower()))
        ).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="email already registered")
        user = User(
            email=body.email.lower(),
            password_hash=hash_password(body.password),
            full_name=body.full_name,
            locale=body.locale if body.locale in {"en", "pt"} else "en",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        user_id = user.id
    refresh = await _issue_refresh(user_id)
    return TokenOut(
        access_token=create_access_token(body.email.lower(), "user"),
        refresh_token=refresh,
    )


@router.post("/login", response_model=TokenOut)
async def login(body: LoginIn) -> TokenOut:
    settings = get_settings()
    factory = get_session_factory()
    async with factory() as session:
        user = (
            await session.execute(select(User).where(User.email == body.email.lower()))
        ).scalar_one_or_none()
        if user and user.locked_until and user.locked_until > datetime.now(UTC):
            LOGIN_TOTAL.labels(result="fail").inc()
            raise HTTPException(status_code=423, detail="account temporarily locked")
        if not user or not verify_password(body.password, user.password_hash):
            if user:
                user.failed_logins = int(user.failed_logins or 0) + 1
                if user.failed_logins >= settings.max_failed_logins:
                    user.locked_until = datetime.now(UTC) + timedelta(minutes=settings.lockout_minutes)
                    user.failed_logins = 0
                await session.commit()
            LOGIN_TOTAL.labels(result="fail").inc()
            raise HTTPException(status_code=401, detail="invalid credentials")
        user.failed_logins = 0
        user.locked_until = None
        await session.commit()
        user_id = user.id
        email = user.email
        role = user.role
    LOGIN_TOTAL.labels(result="ok").inc()
    refresh = await _issue_refresh(user_id)
    return TokenOut(access_token=create_access_token(email, role), refresh_token=refresh)


@router.post("/refresh", response_model=TokenOut)
async def refresh(body: RefreshIn) -> TokenOut:
    factory = get_session_factory()
    async with factory() as session:
        row = (
            await session.execute(
                select(RefreshToken).where(
                    RefreshToken.token_hash == _hash_refresh(body.refresh_token),
                    RefreshToken.revoked == 0,
                )
            )
        ).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=401, detail="invalid refresh token")
        user = (
            await session.execute(select(User).where(User.id == row.user_id))
        ).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="invalid refresh token")
        email, role, user_id = user.email, user.role, user.id
        row.revoked = 1
        await session.commit()
    new_refresh = await _issue_refresh(user_id)
    return TokenOut(access_token=create_access_token(email, role), refresh_token=new_refresh)


@router.post("/logout")
async def logout(body: RefreshIn, user: User = Depends(get_current_user)) -> dict:
    factory = get_session_factory()
    async with factory() as session:
        row = (
            await session.execute(
                select(RefreshToken).where(
                    RefreshToken.token_hash == _hash_refresh(body.refresh_token),
                    RefreshToken.user_id == user.id,
                )
            )
        ).scalar_one_or_none()
        if row:
            row.revoked = 1
            await session.commit()
    return {"logged_out": True}


@router.post("/change-password")
async def change_password(body: ChangePasswordIn, user: User = Depends(get_current_user)) -> dict:
    if not _password_ok(body.new_password):
        raise HTTPException(status_code=400, detail="password too weak")
    if not verify_password(body.current_password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    factory = get_session_factory()
    async with factory() as session:
        db_user = (
            await session.execute(select(User).where(User.id == user.id))
        ).scalar_one()
        db_user.password_hash = hash_password(body.new_password)
        await session.commit()
    return {"changed": True}


@router.get("/me")
async def me(user: User = Depends(get_current_user)) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "locale": user.locale,
    }
