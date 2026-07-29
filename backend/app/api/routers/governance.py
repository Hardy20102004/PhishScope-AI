from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.governance import SecurityPolicy, GovernanceWorkflow, ApprovalRecord, AutomationLog
from app.schemas.governance import (
    SecurityPolicyResponse,
    GovernanceWorkflowResponse,
    ApprovalRecordResponse,
    AutomationLogResponse
)

router = APIRouter()

@router.get("/policies", response_model=List[SecurityPolicyResponse])
async def get_policies(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all security policies.
    """
    res = await db.execute(select(SecurityPolicy).where(SecurityPolicy.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/workflows", response_model=List[GovernanceWorkflowResponse])
async def get_workflows(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all governance workflows.
    """
    res = await db.execute(select(GovernanceWorkflow).where(GovernanceWorkflow.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/approvals", response_model=List[ApprovalRecordResponse])
async def get_approvals(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves approval records.
    """
    res = await db.execute(select(ApprovalRecord).where(ApprovalRecord.tenant_id == current_user.tenant_id))
    return res.scalars().all()
