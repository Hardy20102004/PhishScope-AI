import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.identity_intel import (
    TelemetrySource, TrustLevel, RiskLevel, BehaviorDeviation
)

# ─────────────────────────────────────────────────────────────────────────────
# Telemetry
# ─────────────────────────────────────────────────────────────────────────────
class IdentityTelemetryBase(BaseModel):
    identity_id: str
    source: TelemetrySource
    event_type: str
    context_data: Dict[str, Any] = Field(default_factory=dict)

class IdentityTelemetryCreate(IdentityTelemetryBase):
    pass

class IdentityTelemetryResponse(IdentityTelemetryBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Behavior
# ─────────────────────────────────────────────────────────────────────────────
class BehaviorBaselineResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: str
    typical_devices: List[str]
    typical_locations: List[str]
    typical_active_hours: Dict[str, Any]
    current_deviation: BehaviorDeviation
    last_updated: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Trust Score
# ─────────────────────────────────────────────────────────────────────────────
class AdaptiveTrustScoreResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: str
    composite_score: float
    behavior_confidence: float
    auth_assurance_confidence: float
    hygiene_confidence: float
    trust_level: TrustLevel
    evaluated_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Risk
# ─────────────────────────────────────────────────────────────────────────────
class IdentityRiskAnalyticsResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: str
    overall_risk_score: float
    privilege_risk: float
    operational_risk: float
    risk_level: RiskLevel
    evaluated_at: datetime
    class Config:
        from_attributes = True
