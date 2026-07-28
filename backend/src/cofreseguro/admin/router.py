"""Admin API for demo operations (admin role only)."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, func, select

from cofreseguro.analyze.policy_loader import clear_policy_cache, load_rule_policies, load_url_fragments
from cofreseguro.auth.router import get_current_user
from cofreseguro.shared.database import get_session_factory
from cofreseguro.shared.models import Analysis, User

router = APIRouter(prefix="/v1/admin", tags=["admin"])


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin only")
    return user


@router.get("/users")
async def list_users(admin: User = Depends(require_admin)) -> list[dict]:
    factory = get_session_factory()
    async with factory() as session:
        rows = (await session.execute(select(User).order_by(User.id))).scalars().all()
    return [
        {"id": u.id, "email": u.email, "role": u.role, "locale": u.locale, "full_name": u.full_name}
        for u in rows
    ]


@router.get("/analyses/recent")
async def recent_analyses(limit: int = 50, admin: User = Depends(require_admin)) -> list[dict]:
    factory = get_session_factory()
    async with factory() as session:
        rows = (
            await session.execute(select(Analysis).order_by(desc(Analysis.id)).limit(min(limit, 200)))
        ).scalars().all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "risk_level": r.risk_level,
            "risk_score": r.risk_score,
            "labels": json.loads(r.labels),
            "engine": r.engine,
            "preview": r.text[:100],
        }
        for r in rows
    ]


@router.post("/policies/reload")
async def reload_policies(admin: User = Depends(require_admin)) -> dict:
    clear_policy_cache()
    rules = load_rule_policies()
    urls = load_url_fragments()
    return {"reloaded": True, "rules": len(rules), "url_fragments": len(urls)}


@router.get("/metrics/summary")
async def metrics_summary(admin: User = Depends(require_admin)) -> dict:
    factory = get_session_factory()
    async with factory() as session:
        total = (await session.execute(select(func.count()).select_from(Analysis))).scalar_one()
        users = (await session.execute(select(func.count()).select_from(User))).scalar_one()
        high = (
            await session.execute(
                select(func.count()).select_from(Analysis).where(Analysis.risk_level.in_(["high", "critical"]))
            )
        ).scalar_one()
    return {"users": users, "analyses": total, "high_or_critical": high}
