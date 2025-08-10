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
            profile = BehaviourProfile(user_id=user_id)
            session.add(profile)
        profile.total_analyses += 1
        if risk_level in {"high", "critical"}:
            profile.high_risk_count += 1
        ratio = profile.high_risk_count / max(profile.total_analyses, 1)
        profile.risk_score = min(1.0, ratio * 1.2)
        await session.commit()
        await session.refresh(profile)
        return profile
