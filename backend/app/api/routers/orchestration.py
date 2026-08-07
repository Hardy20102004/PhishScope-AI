from typing import List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.orchestration import (
    WorkflowRecordResponse, PlaybookDefinitionResponse,
    TaskAssignmentResponse, DecisionLogResponse
)
from app.orchestration.workflow_engine import WorkflowEngine
from app.orchestration.playbook_engine import PlaybookEngine
from app.orchestration.task_coordination_engine import TaskCoordinationEngine
from app.orchestration.decision_intelligence_engine import DecisionIntelligenceEngine

router = APIRouter()

@router.get("/workflows", response_model=List[WorkflowRecordResponse])
async def get_workflows(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = WorkflowEngine(db)
    return await engine.get_workflows(current_user.tenant_id)

@router.get("/playbooks", response_model=List[PlaybookDefinitionResponse])
async def get_playbooks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = PlaybookEngine(db)
    return await engine.get_playbooks(current_user.tenant_id)

@router.get("/tasks", response_model=List[TaskAssignmentResponse])
async def get_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = TaskCoordinationEngine(db)
    return await engine.get_tasks(current_user.tenant_id)

@router.get("/decisions", response_model=List[DecisionLogResponse])
async def get_decisions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = DecisionIntelligenceEngine(db)
    return await engine.get_decisions(current_user.tenant_id)
