from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.copilot import (
    ChatMessageRequest,
    CopilotMessageSchema,
    GeneratedReportSchema,
    RecommendationsResponse,
    ReportRequest,
)
from app.services.ai.conversation_manager import ConversationManager
from app.services.ai.recommendation_engine import RecommendationEngine
from app.services.ai.report_generator import ReportGenerator

router = APIRouter()

@router.get("/{investigation_id}/history", response_model=List[CopilotMessageSchema])
def get_history(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    manager = ConversationManager(db)
    messages = manager.get_history(investigation_id)
    return messages

@router.post("/{investigation_id}/chat", response_model=CopilotMessageSchema)
async def chat(
    investigation_id: UUID,
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        manager = ConversationManager(db)
        ai_message = await manager.chat(investigation_id, request.content)
        return ai_message
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{investigation_id}/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(
    investigation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        engine = RecommendationEngine(db)
        recs = await engine.get_recommendations(investigation_id)
        return RecommendationsResponse(recommendations=recs)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{investigation_id}/report", response_model=GeneratedReportSchema)
async def generate_report(
    investigation_id: UUID,
    request: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        generator = ReportGenerator(db)
        report = await generator.generate_report(investigation_id, request.report_type, current_user.id)
        return report
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
