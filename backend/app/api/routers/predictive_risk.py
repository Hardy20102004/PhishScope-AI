from typing import List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.predictive_risk import (
    RiskForecastResponse, StrategicPlanResponse,
    InvestmentScenarioResponse
)
from app.predictive_risk.predictive_risk_engine import PredictiveRiskEngine
from app.predictive_risk.strategic_planning_engine import StrategicPlanningEngine
from app.predictive_risk.investment_prioritization_engine import InvestmentPrioritizationEngine

router = APIRouter()

@router.get("/forecasts", response_model=List[RiskForecastResponse])
async def get_forecasts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = PredictiveRiskEngine(db)
    return await engine.get_forecasts(current_user.tenant_id)

@router.get("/plans", response_model=List[StrategicPlanResponse])
async def get_strategic_plans(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = StrategicPlanningEngine(db)
    return await engine.get_plans(current_user.tenant_id)

@router.get("/investments", response_model=List[InvestmentScenarioResponse])
async def get_investment_scenarios(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = InvestmentPrioritizationEngine(db)
    return await engine.get_scenarios(current_user.tenant_id)
