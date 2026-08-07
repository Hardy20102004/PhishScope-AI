import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.itdr import (
    TelemetryEventType, AttackType, InvestigationStatus,
    IdentityRiskLevel, RecommendationAction
)

# ─────────────────────────────────────────────────────────────────────────────
# Telemetry
# ─────────────────────────────────────────────────────────────────────────────
class ITDRTelemetryEventBase(BaseModel):
    identity_id: str
    event_type: TelemetryEventType
    source_ip: Optional[str] = None
    location: Optional[str] = None
    device_id: Optional[str] = None
    app_name: Optional[str] = None
    status: str
    metadata_json: Dict[str, Any] = Field(default_factory=dict)

class ITDRTelemetryEventCreate(ITDRTelemetryEventBase):
    pass

class ITDRTelemetryEventResponse(ITDRTelemetryEventBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Behavior Baseline
# ─────────────────────────────────────────────────────────────────────────────
class ITDRBehaviorBaselineBase(BaseModel):
    identity_id: str
    frequent_ips: List[str] = Field(default_factory=list)
    frequent_locations: List[str] = Field(default_factory=list)
    frequent_devices: List[str] = Field(default_factory=list)
    typical_active_hours: Dict[str, Any] = Field(default_factory=dict)
    velocity_baseline: float = 0.0

class ITDRBehaviorBaselineResponse(ITDRBehaviorBaselineBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    updated_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Credential Attacks
# ─────────────────────────────────────────────────────────────────────────────
class ITDRCredentialAttackBase(BaseModel):
    attack_type: AttackType
    target_identities: List[str] = Field(default_factory=list)
    source_ips: List[str] = Field(default_factory=list)
    event_count: int = 1
    severity: IdentityRiskLevel = IdentityRiskLevel.HIGH

class ITDRCredentialAttackResponse(ITDRCredentialAttackBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    first_seen: datetime
    last_seen: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Investigations
# ─────────────────────────────────────────────────────────────────────────────
class ITDRInvestigationBase(BaseModel):
    title: str
    description: Optional[str] = None
    primary_identity: str
    linked_telemetry_ids: List[str] = Field(default_factory=list)
    linked_attack_ids: List[str] = Field(default_factory=list)
    assigned_to: Optional[str] = None

class ITDRInvestigationCreate(ITDRInvestigationBase):
    pass

class ITDRInvestigationUpdate(BaseModel):
    status: Optional[InvestigationStatus] = None
    description: Optional[str] = None

class ITDRInvestigationResponse(ITDRInvestigationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: InvestigationStatus
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Risk Scores
# ─────────────────────────────────────────────────────────────────────────────
class ITDRRiskScoreBase(BaseModel):
    identity_id: str
    overall_score: float
    auth_risk: float
    behavior_risk: float
    privilege_risk: float
    risk_level: IdentityRiskLevel
    contributing_factors: List[str] = Field(default_factory=list)

class ITDRRiskScoreResponse(ITDRRiskScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    evaluated_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Recommendations
# ─────────────────────────────────────────────────────────────────────────────
class ITDRRecommendationBase(BaseModel):
    identity_id: str
    investigation_id: Optional[uuid.UUID] = None
    recommended_action: RecommendationAction
    rationale: str
    action_taken: bool = False

class ITDRRecommendationResponse(ITDRRecommendationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True
