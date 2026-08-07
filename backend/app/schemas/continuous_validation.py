import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

class SecurityPostureSnapshotBase(BaseModel):
    overall_posture_score: float
    detection_maturity: float
    response_readiness: float
    control_effectiveness: float

class SecurityPostureSnapshotResponse(SecurityPostureSnapshotBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class SecurityDriftRecordBase(BaseModel):
    drift_type: str
    severity: str
    description: str
    baseline_value: float
    current_value: float
    is_acknowledged: bool

class SecurityDriftRecordResponse(SecurityDriftRecordBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class OptimizationRecommendationBase(BaseModel):
    title: str
    description: str
    domain: str
    priority: str
    expected_score_improvement: float
    status: str

class OptimizationRecommendationResponse(OptimizationRecommendationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
