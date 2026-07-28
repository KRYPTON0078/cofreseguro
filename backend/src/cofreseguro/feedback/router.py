"""User feedback on analysis quality (false positive / negative)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from cofreseguro.auth.router import get_current_user
from cofreseguro.shared.database import get_session_factory
from cofreseguro.shared.models import Analysis, Feedback, User

router = APIRouter(prefix="/v1/feedback", tags=["feedback"])


class FeedbackIn(BaseModel):
    analysis_id: int
    verdict: str = Field(pattern="^(false_positive|false_negative|correct)$")
    note: str = Field(default="", max_length=500)


@router.post("")
async def submit_feedback(body: FeedbackIn, user: User = Depends(get_current_user)) -> dict:
    factory = get_session_factory()
    async with factory() as session:
        analysis = (
            await session.execute(
                select(Analysis).where(Analysis.id == body.analysis_id, Analysis.user_id == user.id)
            )
        ).scalar_one_or_none()
        if not analysis:
            raise HTTPException(status_code=404, detail="analysis not found")
        row = Feedback(
            analysis_id=body.analysis_id,
            user_id=user.id,
            verdict=body.verdict,
            note=body.note,
        )
        session.add(row)
        await session.commit()
        await session.refresh(row)
        return {"id": row.id, "verdict": row.verdict}
