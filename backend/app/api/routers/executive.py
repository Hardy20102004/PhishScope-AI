import uuid
from typing import Any, List, Dict
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.executive import (
    ExecutiveMetricResponse,
    BusinessRiskScoreResponse,
    ExecutiveReportResponse
)

from app.executive.analytics_engine import AnalyticsEngine
from app.executive.risk_engine import RiskEngine
from app.executive.ai_executive_assistant import AIExecutiveAssistant

router = APIRouter()

@router.get("/kpis", response_model=Dict[str, float])
async def get_macro_kpis(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Fetch high-level SOC KPIs (MTTR, Incident Volume, etc).
    """
    engine = AnalyticsEngine(db)
    return await engine.get_kpis(current_user.tenant_id)

@router.get("/risk", response_model=List[Dict[str, Any]])
async def get_business_risk(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Fetch computed risk scores by Business Unit.
    """
    engine = RiskEngine(db)
    return await engine.calculate_business_risk(current_user.tenant_id)

@router.post("/reports/generate", response_model=ExecutiveReportResponse)
async def generate_board_report(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate an AI-driven Board Report summarizing the month's security posture.
    """
    engine = AIExecutiveAssistant(db)
    return await engine.generate_board_report(current_user.tenant_id)
