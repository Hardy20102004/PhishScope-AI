from typing import List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.identity_command_center import (
    EnterpriseIdentityPortfolioResponse, IdentityHealthMetricResponse,
    ExecutiveDecisionLogResponse
)
from app.identity_command_center.command_center_manager import CommandCenterManager
from app.identity_command_center.executive_decision_engine import ExecutiveDecisionEngine

router = APIRouter()

@router.get("/portfolio", response_model=List[EnterpriseIdentityPortfolioResponse])
async def get_portfolio(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    manager = CommandCenterManager(db)
    return await manager.get_portfolio(current_user.tenant_id)

@router.get("/health", response_model=List[IdentityHealthMetricResponse])
async def get_health_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    manager = CommandCenterManager(db)
    return await manager.get_health_metrics(current_user.tenant_id)

@router.get("/decisions", response_model=List[ExecutiveDecisionLogResponse])
async def get_decisions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ExecutiveDecisionEngine(db)
    return await engine.get_decision_logs(current_user.tenant_id)
