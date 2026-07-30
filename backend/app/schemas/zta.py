import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.zta import (
    VerificationType, AccessDecision, SessionStatus,
    PolicyEffect, RiskLevel, DeviceTrustStatus
)


# ─────────────────────────────────────────────────────────────────────────────
# ZTA Context Snapshot
# ─────────────────────────────────────────────────────────────────────────────
class ZTAContextSnapshotBase(BaseModel):
    identity_id: Optional[str] = None
    device_id: Optional[str] = None
    session_id: Optional[str] = None
    application_id: Optional[str] = None
    identity_context: Dict[str, Any] = Field(default_factory=dict)
    device_context: Dict[str, Any] = Field(default_factory=dict)
    network_context: Dict[str, Any] = Field(default_factory=dict)
    location_context: Dict[str, Any] = Field(default_factory=dict)
    auth_context: Dict[str, Any] = Field(default_factory=dict)

class ZTAContextSnapshotCreate(ZTAContextSnapshotBase):
    pass

class ZTAContextSnapshotResponse(ZTAContextSnapshotBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    evaluated_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Verification Record
# ─────────────────────────────────────────────────────────────────────────────
class ZTAVerificationRecordBase(BaseModel):
    verification_type: VerificationType
    entity_id: str
    is_valid: bool
    findings: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_score: float

class ZTAVerificationRecordCreate(ZTAVerificationRecordBase):
    context_snapshot_id: uuid.UUID

class ZTAVerificationRecordResponse(ZTAVerificationRecordBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    context_snapshot_id: uuid.UUID
    verified_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Policies
# ─────────────────────────────────────────────────────────────────────────────
class ZTAPolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    priority: int = 100
    conditions: Dict[str, Any] = Field(default_factory=dict)
    effect: PolicyEffect
    actions: List[str] = Field(default_factory=list)

class ZTAPolicyCreate(ZTAPolicyBase):
    pass

class ZTAPolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    conditions: Optional[Dict[str, Any]] = None
    effect: Optional[PolicyEffect] = None
    actions: Optional[List[str]] = None

class ZTAPolicyResponse(ZTAPolicyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Access Decisions
# ─────────────────────────────────────────────────────────────────────────────
class ZTAAccessDecisionBase(BaseModel):
    decision: AccessDecision
    matched_policy_ids: List[str] = Field(default_factory=list)
    rationale: Optional[str] = None
    resource_requested: str

class ZTAAccessDecisionCreate(ZTAAccessDecisionBase):
    context_snapshot_id: uuid.UUID

class ZTAAccessDecisionResponse(ZTAAccessDecisionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    context_snapshot_id: uuid.UUID
    evaluated_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────────────────────
class ZTASessionStateBase(BaseModel):
    session_identifier: str
    identity_id: str
    device_id: Optional[str] = None
    status: SessionStatus = SessionStatus.ACTIVE
    current_session_risk: RiskLevel = RiskLevel.LOW
    risk_score: float = 0.0
    anomalies_detected: int = 0
    expires_at: Optional[datetime] = None

class ZTASessionStateCreate(ZTASessionStateBase):
    pass

class ZTASessionStateUpdate(BaseModel):
    status: Optional[SessionStatus] = None
    current_session_risk: Optional[RiskLevel] = None
    risk_score: Optional[float] = None
    anomalies_detected: Optional[int] = None
    last_verified_at: Optional[datetime] = None

class ZTASessionStateResponse(ZTASessionStateBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    started_at: datetime
    last_verified_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Risk Evaluation
# ─────────────────────────────────────────────────────────────────────────────
class ZTARiskEvaluationBase(BaseModel):
    identity_risk_score: float
    device_risk_score: float
    session_risk_score: float
    app_risk_score: float
    composite_risk_score: float
    risk_level: RiskLevel
    contributing_factors: List[str] = Field(default_factory=list)
    confidence: float

class ZTARiskEvaluationCreate(ZTARiskEvaluationBase):
    context_snapshot_id: uuid.UUID

class ZTARiskEvaluationResponse(ZTARiskEvaluationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    context_snapshot_id: uuid.UUID
    evaluated_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Policy Approval Workflow
# ─────────────────────────────────────────────────────────────────────────────
class ZTAPolicyApprovalBase(BaseModel):
    requested_by: str
    requested_changes: Dict[str, Any]
    justification: str
    status: str = "PENDING"
    approved_by: Optional[str] = None

class ZTAPolicyApprovalCreate(ZTAPolicyApprovalBase):
    policy_id: uuid.UUID

class ZTAPolicyApprovalResponse(ZTAPolicyApprovalBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    policy_id: uuid.UUID
    created_at: datetime
    resolved_at: Optional[datetime] = None
    class Config:
        from_attributes = True
