"""SQLAlchemy models."""

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(128), default="")
    role: Mapped[str] = mapped_column(String(32), default="user")
    locale: Mapped[str] = mapped_column(String(8), default="en")
    failed_logins: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True, default=0)
    text: Mapped[str] = mapped_column(Text)
    locale: Mapped[str] = mapped_column(String(8), default="en")
    risk_level: Mapped[str] = mapped_column(String(16), index=True)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    labels: Mapped[str] = mapped_column(Text, default="[]")
    explanation: Mapped[str] = mapped_column(Text, default="")
    tip: Mapped[str] = mapped_column(Text, default="")
    engine: Mapped[str] = mapped_column(String(64), default="rules")
    engine_scores: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BehaviourProfile(Base):
    __tablename__ = "behaviour_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    high_risk_count: Mapped[int] = mapped_column(Integer, default=0)
    total_analyses: Mapped[int] = mapped_column(Integer, default=0)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UrlCheck(Base):
    __tablename__ = "url_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    analysis_id: Mapped[int] = mapped_column(Integer, index=True, default=0)
    url: Mapped[str] = mapped_column(String(1024))
    score: Mapped[float] = mapped_column(Float, default=0.0)
    reasons: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    analysis_id: Mapped[int] = mapped_column(Integer, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    verdict: Mapped[str] = mapped_column(String(32))
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    revoked: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
