from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.cyber_resilience import ExecutiveKPI
from app.schemas.cyber_resilience import (
    CyberResilienceScoreResponse,
    MaturityAssessmentResponse,
    ExecutiveKPIResponse
)

from app.cyber_resilience.scoring_engine import SecurityScoringEngine
from app.cyber_resilience.maturity_engine import MaturityAssessmentEngine

router = APIRouter()

@router.get("/score", response_model=CyberResilienceScoreResponse)
async def get_cyber_resilience_score(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the apex Cyber Resilience Score.
    """
    eng = SecurityScoringEngine(db)
    # Simulate aggregation for MVP
    score = await eng.generate_resilience_score(current_user.tenant_id, 88.0, 75.0, 82.0)
    return score

@router.get("/maturity/{domain}", response_model=MaturityAssessmentResponse)
async def get_domain_maturity(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    domain: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Evaluates and returns the maturity tier for a specific domain.
    """
    eng = MaturityAssessmentEngine(db)
    # Simulate calculating from an operational score of 78
    return await eng.calculate_domain_maturity(current_user.tenant_id, domain, 78.0)

@router.get("/kpis", response_model=List[ExecutiveKPIResponse])
async def get_executive_kpis(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves board-level KPIs.
    """
    res = await db.execute(select(ExecutiveKPI).where(ExecutiveKPI.tenant_id == current_user.tenant_id))
    return res.scalars().all()
