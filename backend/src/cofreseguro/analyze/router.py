"""Analyze API routes."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy import desc, select

from cofreseguro.analyze.ocr import extract_text_from_image
from cofreseguro.analyze.pipeline import analyze_text
from cofreseguro.auth.router import get_current_user
from cofreseguro.behaviour.profile import update_behaviour
from cofreseguro.shared.database import get_session_factory
from cofreseguro.shared.metrics import ANALYSES_TOTAL
from cofreseguro.shared.models import Analysis, UrlCheck, User

router = APIRouter(prefix="/v1", tags=["analyze"])


class AnalyzeIn(BaseModel):
    text: str = Field(min_length=1, max_length=8000)
    locale: str = "en"


class AnalyzeOut(BaseModel):
    id: int
    risk_score: float
    risk_level: str
    labels: list[str]
    explanation: str
    tip: str
    engine: str
    url_scores: list[dict]


@router.post("/analyze", response_model=AnalyzeOut)
async def analyze(body: AnalyzeIn, user: User = Depends(get_current_user)) -> AnalyzeOut:
    locale = body.locale if body.locale in {"en", "pt"} else user.locale
    result = await analyze_text(body.text, locale)
    factory = get_session_factory()
    async with factory() as session:
        row = Analysis(
            user_id=user.id,
            text=body.text,
            locale=locale,
            risk_level=result.risk_level,
            risk_score=result.risk_score,
            labels=json.dumps(result.labels),
            explanation=result.explanation,
            tip=result.tip,
            engine=result.engine,
        )
        session.add(row)
        await session.flush()
        for u in result.url_scores:
            session.add(
                UrlCheck(
                    analysis_id=row.id,
                    url=str(u.get("url", "")),
                    score=float(u.get("score", 0.0)),
                    reasons=json.dumps(u.get("reasons") or []),
                )
            )
        await session.commit()
        await session.refresh(row)
        analysis_id = row.id
    await update_behaviour(user.id, result.risk_level)
    ANALYSES_TOTAL.labels(risk_level=result.risk_level).inc()
    return AnalyzeOut(
        id=analysis_id,
        risk_score=result.risk_score,
        risk_level=result.risk_level,
        labels=result.labels,
        explanation=result.explanation,
        tip=result.tip,
        engine=result.engine,
        url_scores=result.url_scores,
    )


@router.post("/analyze/image", response_model=AnalyzeOut)
async def analyze_image(
    file: UploadFile = File(...),
    locale: str = "en",
    user: User = Depends(get_current_user),
) -> AnalyzeOut:
    data = await file.read()
    text, available = extract_text_from_image(data)
    if not available or not text:
        text = "[ocr_unavailable] Please paste the SMS text manually."
    return await analyze(AnalyzeIn(text=text, locale=locale), user)


@router.get("/history")
async def history(limit: int = 20, user: User = Depends(get_current_user)) -> list[dict]:
    factory = get_session_factory()
    async with factory() as session:
        rows = (
            await session.execute(
                select(Analysis)
                .where(Analysis.user_id == user.id)
                .order_by(desc(Analysis.id))
                .limit(min(limit, 100))
            )
        ).scalars().all()
    return [
        {
            "id": r.id,
            "risk_level": r.risk_level,
            "risk_score": r.risk_score,
            "labels": json.loads(r.labels),
            "tip": r.tip,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "text_preview": r.text[:120],
            "engine": r.engine,
        }
        for r in rows
    ]
