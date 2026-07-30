import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.cyber_resilience import (
    CriticalityTier, TestOutcome, ExerciseStatus
)

# ─────────────────────────────────────────────────────────────────────────────
# Business Continuity
# ─────────────────────────────────────────────────────────────────────────────
class BusinessServiceNodeBase(BaseModel):
    service_name: str
    description: Optional[str] = None
    tier: CriticalityTier
    dependencies: List[str] = Field(default_factory=list)

class BusinessServiceNodeResponse(BusinessServiceNodeBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True

class RecoveryObjectiveBase(BaseModel):
    service_id: uuid.UUID
    rto_minutes: int
    rpo_minutes: int

class RecoveryObjectiveResponse(RecoveryObjectiveBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    last_validated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Disaster Recovery & Tabletops
# ─────────────────────────────────────────────────────────────────────────────
class DisasterRecoveryTestBase(BaseModel):
    test_name: str
    scope: str
    outcome: TestOutcome
    actual_rto_minutes: Optional[int] = None
    findings: List[Dict[str, Any]] = Field(default_factory=list)

class DisasterRecoveryTestResponse(DisasterRecoveryTestBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    tested_at: datetime
    class Config:
        from_attributes = True

class TabletopExerciseBase(BaseModel):
    title: str
    scenario_description: str
    status: ExerciseStatus
    participants: List[str] = Field(default_factory=list)
    lessons_learned: List[Dict[str, Any]] = Field(default_factory=list)
    scheduled_for: Optional[datetime] = None

class TabletopExerciseResponse(TabletopExerciseBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Readiness Aggregation
# ─────────────────────────────────────────────────────────────────────────────
class ResilienceAssessmentBase(BaseModel):
    overall_readiness_score: float
    domain_scores: Dict[str, float] = Field(default_factory=dict)

class ResilienceAssessmentResponse(ResilienceAssessmentBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    assessed_at: datetime
    class Config:
        from_attributes = True
