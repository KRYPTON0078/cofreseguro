"""Auth routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from cofreseguro.auth.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)
from cofreseguro.shared.database import get_session_factory
from cofreseguro.shared.metrics import LOGIN_TOTAL
from cofreseguro.shared.models import User

router = APIRouter(prefix="/v1/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    full_name: str = ""
    locale: str = "en"


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


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
    factory = get_session_factory()
    async with factory() as session:
        existing = (
            await session.execute(select(User).where(User.email == body.email))
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
    return TokenOut(access_token=create_access_token(body.email.lower(), "user"))


@router.post("/login", response_model=TokenOut)
async def login(body: LoginIn) -> TokenOut:
    factory = get_session_factory()
    async with factory() as session:
        user = (
            await session.execute(select(User).where(User.email == body.email.lower()))
        ).scalar_one_or_none()
    if not user or not verify_password(body.password, user.password_hash):
        LOGIN_TOTAL.labels(result="fail").inc()
        raise HTTPException(status_code=401, detail="invalid credentials")
    LOGIN_TOTAL.labels(result="ok").inc()
    return TokenOut(access_token=create_access_token(user.email, user.role))


@router.get("/me")
async def me(user: User = Depends(get_current_user)) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "locale": user.locale,
    }
