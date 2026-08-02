"""Behavioural risk API."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select

from cofreseguro.auth.router import get_current_user
from cofreseguro.shared.database import get_session_factory
from cofreseguro.shared.models import BehaviourProfile, User

router = APIRouter(prefix="/v1/behaviour", tags=["behaviour"])


@router.get("/me")
async def my_behaviour(user: User = Depends(get_current_user)) -> dict:
    factory = get_session_factory()
    async with factory() as session:
        profile = (
            await session.execute(
                select(BehaviourProfile).where(BehaviourProfile.user_id == user.id)
            )
        ).scalar_one_or_none()
    if profile is None:
        return {
            "user_id": user.id,
            "total_analyses": 0,
            "high_risk_count": 0,
            "risk_score": 0.0,
        }
    return {
        "user_id": user.id,
        "total_analyses": profile.total_analyses,
        "high_risk_count": profile.high_risk_count,
        "risk_score": profile.risk_score,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
    }
