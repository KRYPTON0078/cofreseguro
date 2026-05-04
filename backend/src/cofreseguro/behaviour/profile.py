"""Per-user behavioural risk tracking."""

from __future__ import annotations

from sqlalchemy import select

from cofreseguro.shared.database import get_session_factory
from cofreseguro.shared.models import BehaviourProfile


async def update_behaviour(user_id: int, risk_level: str) -> BehaviourProfile:
    factory = get_session_factory()
    async with factory() as session:
        profile = (
            await session.execute(
                select(BehaviourProfile).where(BehaviourProfile.user_id == user_id)
            )
        ).scalar_one_or_none()
        if profile is None:
            profile = BehaviourProfile(
                user_id=user_id,
                high_risk_count=0,
                total_analyses=0,
                risk_score=0.0,
            )
            session.add(profile)
        total = int(profile.total_analyses or 0) + 1
        high = int(profile.high_risk_count or 0)
        if risk_level in {"high", "critical"}:
            high += 1
        profile.total_analyses = total
        profile.high_risk_count = high
        ratio = high / max(total, 1)
        profile.risk_score = min(1.0, ratio * 1.2)
        await session.commit()
        await session.refresh(profile)
        return profile
