import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.cyber_fusion import (
    FusionRecordType, CyberRiskLevel, RecommendationStatus
)

# ─────────────────────────────────────────────────────────────────────────────
# Fusion Record
# ─────────────────────────────────────────────────────────────────────────────
class FusionRecordBase(BaseModel):
    record_type: FusionRecordType
    title: str
    description: Optional[str] = None
    source_modules: List[str]
    correlated_entities: List[str]
    risk_level: CyberRiskLevel

class FusionRecordResponse(FusionRecordBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Risk Scores
# ─────────────────────────────────────────────────────────────────────────────
class CrossDomainRiskScoreResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    enterprise_risk_index: float
    identity_risk_factor: float
    cloud_risk_factor: float
    appsec_risk_factor: float
    network_risk_factor: float
    measured_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Recommendations
# ─────────────────────────────────────────────────────────────────────────────
class StrategicRecommendationBase(BaseModel):
    fusion_record_id: Optional[uuid.UUID] = None
    recommendation_text: str
    strategic_impact: Optional[str] = None

class StrategicRecommendationCreate(StrategicRecommendationBase):
    pass

class StrategicRecommendationResponse(StrategicRecommendationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: RecommendationStatus
    approved_by: Optional[str] = None
    generated_at: datetime
    resolved_at: Optional[datetime]
    class Config:
        from_attributes = True
