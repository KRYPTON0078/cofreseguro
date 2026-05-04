"""Password hashing and JWT."""

from datetime import UTC, datetime, timedelta

import bcrypt
from jose import JWTError, jwt
from pydantic import BaseModel

from cofreseguro.shared.config import get_settings


class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: datetime


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(email: str, role: str) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode(
        {"sub": email, "role": role, "exp": expire},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_token(token: str) -> TokenPayload:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return TokenPayload(
            sub=payload["sub"],
            role=payload.get("role", "user"),
            exp=datetime.fromtimestamp(payload["exp"], tz=UTC),
        )
    except (JWTError, KeyError, ValueError) as exc:
        raise ValueError("invalid token") from exc
