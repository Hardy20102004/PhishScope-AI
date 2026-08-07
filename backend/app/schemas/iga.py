import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.iga import (
    JMLEventType, JMLStatus, AccessRequestStatus, CertificationStatus,
    CertificationDecision, SoDSeverity, RiskLevel
)

# ─────────────────────────────────────────────────────────────────────────────
# Joiner-Mover-Leaver
# ─────────────────────────────────────────────────────────────────────────────
class IGALifecycleEventBase(BaseModel):
    identity_id: str
    event_type: JMLEventType
    source_system: str
    effective_date: datetime
    metadata_json: Dict[str, Any] = Field(default_factory=dict)

class IGALifecycleEventCreate(IGALifecycleEventBase):
    pass

class IGALifecycleEventResponse(IGALifecycleEventBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: JMLStatus
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Access Request
# ─────────────────────────────────────────────────────────────────────────────
class IGAAccessRequestBase(BaseModel):
    requester_id: str
    target_identity_id: str
    entitlement_id: str
    justification: str
    expires_at: Optional[datetime] = None

class IGAAccessRequestCreate(IGAAccessRequestBase):
    pass

class IGAAccessRequestResponse(IGAAccessRequestBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: AccessRequestStatus
    approver_id: Optional[str] = None
    approval_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Certifications
# ─────────────────────────────────────────────────────────────────────────────
class IGACertificationCampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: datetime

class IGACertificationCampaignCreate(IGACertificationCampaignBase):
    pass

class IGACertificationCampaignResponse(IGACertificationCampaignBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: CertificationStatus
    start_date: datetime
    total_items: int
    completed_items: int
    class Config:
        from_attributes = True

class IGACertificationItemResponse(BaseModel):
    id: uuid.UUID
    campaign_id: uuid.UUID
    identity_id: str
    entitlement_id: str
    reviewer_id: str
    decision: Optional[CertificationDecision] = None
    decision_notes: Optional[str] = None
    decision_date: Optional[datetime] = None
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Segregation of Duties
# ─────────────────────────────────────────────────────────────────────────────
class IGASegregationOfDutiesRuleBase(BaseModel):
    name: str
    description: str
    conflicting_entitlements: List[str]
    severity: SoDSeverity
    active: bool = True

class IGASegregationOfDutiesRuleCreate(IGASegregationOfDutiesRuleBase):
    pass

class IGASegregationOfDutiesRuleResponse(IGASegregationOfDutiesRuleBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    class Config:
        from_attributes = True

class IGASoDViolationResponse(BaseModel):
    id: uuid.UUID
    rule_id: uuid.UUID
    identity_id: str
    detected_at: datetime
    resolved: bool
    resolution_notes: Optional[str] = None
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Risk Scores
# ─────────────────────────────────────────────────────────────────────────────
class IGARiskScoreResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: str
    overall_score: float
    access_risk: float
    sod_risk: float
    risk_level: RiskLevel
    evaluated_at: datetime
    class Config:
        from_attributes = True
