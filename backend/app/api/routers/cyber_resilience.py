from typing import List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.cyber_resilience import (
    BusinessServiceNodeResponse, DisasterRecoveryTestResponse,
    TabletopExerciseResponse, ResilienceAssessmentResponse
)
from app.cyber_resilience.business_continuity_engine import BusinessContinuityEngine
from app.cyber_resilience.disaster_recovery_engine import DisasterRecoveryEngine
from app.cyber_resilience.tabletop_exercise_engine import TabletopExerciseEngine
from app.cyber_resilience.readiness_assessment_engine import ReadinessAssessmentEngine

router = APIRouter()

@router.get("/business-services", response_model=List[BusinessServiceNodeResponse])
async def get_business_services(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = BusinessContinuityEngine(db)
    return await engine.get_services(current_user.tenant_id)

@router.get("/dr-tests", response_model=List[DisasterRecoveryTestResponse])
async def get_dr_tests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = DisasterRecoveryEngine(db)
    return await engine.get_dr_tests(current_user.tenant_id)

@router.get("/tabletops", response_model=List[TabletopExerciseResponse])
async def get_tabletop_exercises(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = TabletopExerciseEngine(db)
    return await engine.get_exercises(current_user.tenant_id)

@router.get("/assessments", response_model=List[ResilienceAssessmentResponse])
async def get_assessments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ReadinessAssessmentEngine(db)
    return await engine.get_assessments(current_user.tenant_id)
