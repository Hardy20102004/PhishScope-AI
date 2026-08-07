import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api import deps
from app.models.user import User
from app.models.soar import Playbook, ExecutionHistory, ApprovalRecord
from app.schemas.soar import (
    PlaybookCreate, PlaybookResponse, ExecutionHistoryResponse, ExecutionHistoryCreate,
    ApprovalRecordResponse, ApprovalReview
)

from app.soar.playbook_manager import PlaybookManager
from app.soar.execution_engine import ExecutionEngine
from app.soar.approval_engine import ApprovalEngine

router = APIRouter()

@router.post("/playbooks", response_model=PlaybookResponse, status_code=status.HTTP_201_CREATED)
async def create_playbook(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    playbook_in: PlaybookCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new visual Playbook.
    """
    manager = PlaybookManager(db)
    playbook = await manager.create_playbook(
        name=playbook_in.name,
        description=playbook_in.description,
        tenant_id=current_user.tenant_id
    )
    return playbook

@router.get("/playbooks", response_model=List[PlaybookResponse])
async def list_playbooks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(
        select(Playbook)
        .where(Playbook.tenant_id == current_user.tenant_id)
        .order_by(Playbook.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/playbooks/{playbook_id}/execute", response_model=ExecutionHistoryResponse)
async def execute_playbook(
    playbook_id: uuid.UUID,
    exec_in: ExecutionHistoryCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Triggers the Execution Engine for a specific Playbook.
    """
    engine = ExecutionEngine(db)
    execution = await engine.start_execution(playbook_id, exec_in.incident_id)
    
    # Reload with approvals
    result = await db.execute(
        select(ExecutionHistory)
        .options(selectinload(ExecutionHistory.approvals))
        .where(ExecutionHistory.id == execution.id)
    )
    return result.scalar_one()

@router.post("/approvals/{approval_id}/review", response_model=ApprovalRecordResponse)
async def review_approval(
    approval_id: uuid.UUID,
    review_in: ApprovalReview,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Submit an analyst review for a workflow blocked on a manual Approval Gate.
    """
    engine = ApprovalEngine(db)
    approval = await engine.process_approval(
        approval_id=approval_id,
        user_id=current_user.id,
        approved=review_in.approved,
        notes=review_in.notes
    )
    return approval
