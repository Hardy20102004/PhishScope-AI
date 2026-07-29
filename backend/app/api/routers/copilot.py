from typing import Any, List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api import deps
from app.models.user import User
from app.models.copilot import CodeReviewRecord, DeveloperCopilotSession
from app.schemas.copilot import (
    DeveloperCopilotSessionCreate, DeveloperCopilotSessionResponse,
    CodeReviewRecordCreate, CodeReviewRecordResponse,
    CodeReviewFindingCreate, CodeReviewFindingResponse,
    DeveloperLearningProgressCreate, DeveloperLearningProgressResponse,
    EngineeringMetricCreate, EngineeringMetricResponse
)

from app.copilot.developer_copilot_engine import DeveloperCopilotEngine
from app.copilot.ai_code_review_engine import AICodeReviewEngine
from app.copilot.engineering_intelligence_engine import EngineeringIntelligenceEngine
from app.copilot.learning_knowledge_engine import LearningKnowledgeEngine

router = APIRouter()

@router.post("/sessions", response_model=DeveloperCopilotSessionResponse)
async def init_session(
    session_in: DeveloperCopilotSessionCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DeveloperCopilotEngine(db)
    return await engine.initialize_session(current_user.tenant_id, current_user.id, session_in)

@router.post("/review", response_model=CodeReviewRecordResponse)
async def submit_review(
    review_in: CodeReviewRecordCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = AICodeReviewEngine(db)
    return await engine.submit_review(current_user.tenant_id, review_in)

@router.post("/review/findings", response_model=CodeReviewFindingResponse)
async def add_review_finding(
    finding_in: CodeReviewFindingCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = AICodeReviewEngine(db)
    return await engine.add_finding(current_user.tenant_id, finding_in)

@router.get("/review", response_model=List[CodeReviewRecordResponse])
async def list_reviews(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = AICodeReviewEngine(db)
    return await engine.list_reviews(current_user.tenant_id)

@router.post("/intelligence", response_model=EngineeringMetricResponse)
async def register_metric(
    metric_in: EngineeringMetricCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = EngineeringIntelligenceEngine(db)
    return await engine.register_metric(current_user.tenant_id, metric_in)

@router.get("/intelligence", response_model=List[EngineeringMetricResponse])
async def get_metrics(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = EngineeringIntelligenceEngine(db)
    return await engine.get_metrics(current_user.tenant_id)

@router.post("/learning", response_model=DeveloperLearningProgressResponse)
async def update_learning(
    progress_in: DeveloperLearningProgressCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = LearningKnowledgeEngine(db)
    return await engine.update_progress(current_user.tenant_id, current_user.id, progress_in)

@router.get("/learning", response_model=List[DeveloperLearningProgressResponse])
async def get_learning(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = LearningKnowledgeEngine(db)
    return await engine.get_learning_profile(current_user.tenant_id, current_user.id)
