import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api import deps
from app.models.user import User
from app.models.ai_triage import AITriageGroup, AlertRecommendation, AnalystFeedback
from app.schemas.ai_triage import AITriageGroupResponse, AnalystFeedbackCreate, AnalystFeedbackResponse

from app.ai_triage.triage_manager import AITriageManager
from app.ai_triage.feedback import FeedbackLearningEngine

router = APIRouter()

@router.post("/process-batch", response_model=AITriageGroupResponse)
async def process_alert_batch(
    alert_ids: List[uuid.UUID],
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Manually trigger AI triage grouping and prioritization on a batch of raw alerts.
    """
    manager = AITriageManager(db)
    group = await manager.triage_alert_batch(alert_ids, current_user.tenant_id)
    
    # Reload with relationships
    result = await db.execute(
        select(AITriageGroup)
        .options(selectinload(AITriageGroup.recommendation))
        .where(AITriageGroup.id == group.id)
    )
    return result.scalar_one()

@router.get("/groups", response_model=List[AITriageGroupResponse])
async def list_triage_groups(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    List AI Triage Groups for the SOC Dashboard queue.
    """
    result = await db.execute(
        select(AITriageGroup)
        .options(selectinload(AITriageGroup.recommendation))
        .where(AITriageGroup.tenant_id == current_user.tenant_id)
        .order_by(AITriageGroup.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/groups/{group_id}/feedback", response_model=AnalystFeedbackResponse)
async def submit_analyst_feedback(
    group_id: uuid.UUID,
    feedback_in: AnalystFeedbackCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Submit feedback on an AI grouping or recommendation to train the learning engine.
    """
    engine = FeedbackLearningEngine(db)
    feedback = await engine.record_feedback(
        triage_group_id=group_id,
        user_id=current_user.id,
        feedback_type=feedback_in.feedback_type,
        comments=feedback_in.comments
    )
    
    # Apply override immediately if requested
    if feedback_in.priority_override:
        result = await db.execute(select(AITriageGroup).where(AITriageGroup.id == group_id))
        group = result.scalar_one_or_none()
        if group:
            group.priority_tier = feedback_in.priority_override
            await db.commit()
            
    return feedback
