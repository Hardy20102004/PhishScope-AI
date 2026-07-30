import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.authn import (
    AuthnMethodType, EnrollmentStatus, AssuranceLevel, RiskLevel
)

# ─────────────────────────────────────────────────────────────────────────────
# Authn Methods
# ─────────────────────────────────────────────────────────────────────────────
class AuthnMethodBase(BaseModel):
    name: str
    type: AuthnMethodType
    provider: str
    is_phishing_resistant: bool = False
    metadata_json: Dict[str, Any] = Field(default_factory=dict)

class AuthnMethodCreate(AuthnMethodBase):
    pass

class AuthnMethodResponse(AuthnMethodBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Enrollments
# ─────────────────────────────────────────────────────────────────────────────
class AuthnEnrollmentBase(BaseModel):
    identity_id: str
    method_id: uuid.UUID
    device_id: Optional[str] = None
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE

class AuthnEnrollmentCreate(AuthnEnrollmentBase):
    pass

class AuthnEnrollmentResponse(AuthnEnrollmentBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    last_used_at: Optional[datetime] = None
    enrolled_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Policies & Assurance
# ─────────────────────────────────────────────────────────────────────────────
class AuthnPolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_group: str
    required_aal: AssuranceLevel
    active: bool = True

class AuthnPolicyResponse(AuthnPolicyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    class Config:
        from_attributes = True

class AuthnAssuranceLevelResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: str
    current_aal: AssuranceLevel
    highest_capable_aal: AssuranceLevel
    evaluated_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Risk
# ─────────────────────────────────────────────────────────────────────────────
class AuthnRiskScoreResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: str
    overall_score: float
    weak_mfa_risk: float
    recovery_risk: float
    risk_level: RiskLevel
    evaluated_at: datetime
    class Config:
        from_attributes = True
