import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.pam import (
    PrivilegedIdentityType, JITRequestStatus, AdminSessionStatus,
    CredentialStatus, PrivilegeRiskLevel
)

# ─────────────────────────────────────────────────────────────────────────────
# Privileged Identity
# ─────────────────────────────────────────────────────────────────────────────
class PAMPrivilegedIdentityBase(BaseModel):
    ispm_identity_id: Optional[str] = None
    identity_type: PrivilegedIdentityType
    display_name: str
    principal_name: str
    source_platform: str
    is_standing_privilege: bool = True
    owner_email: Optional[str] = None
    business_justification: Optional[str] = None
    privilege_risk_score: float = 0.0
    risk_level: PrivilegeRiskLevel = PrivilegeRiskLevel.LOW

class PAMPrivilegedIdentityCreate(PAMPrivilegedIdentityBase):
    pass

class PAMPrivilegedIdentityResponse(PAMPrivilegedIdentityBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    last_reviewed_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# JIT Request
# ─────────────────────────────────────────────────────────────────────────────
class PAMJITRequestBase(BaseModel):
    requester_id: str
    target_role: str
    target_resource: str
    justification: str
    ticket_reference: Optional[str] = None
    requested_duration_minutes: int = 60

class PAMJITRequestCreate(PAMJITRequestBase):
    pass

class PAMJITRequestUpdate(BaseModel):
    status: Optional[JITRequestStatus] = None
    approved_by: Optional[str] = None
    approval_notes: Optional[str] = None
    activated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

class PAMJITRequestResponse(PAMJITRequestBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: JITRequestStatus
    approved_by: Optional[str] = None
    approval_notes: Optional[str] = None
    created_at: datetime
    activated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Admin Session
# ─────────────────────────────────────────────────────────────────────────────
class PAMSessionRecordBase(BaseModel):
    jit_request_id: Optional[uuid.UUID] = None
    identity_id: str
    target_resource: str
    ip_address: Optional[str] = None
    mfa_verified: bool = True
    session_risk_score: float = 0.0
    recording_vault_reference: Optional[str] = None

class PAMSessionRecordCreate(PAMSessionRecordBase):
    pass

class PAMSessionRecordUpdate(BaseModel):
    status: Optional[AdminSessionStatus] = None
    ended_at: Optional[datetime] = None

class PAMSessionRecordResponse(PAMSessionRecordBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: AdminSessionStatus
    started_at: datetime
    ended_at: Optional[datetime] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Credential Lifecycle
# ─────────────────────────────────────────────────────────────────────────────
class PAMCredentialLifecycleBase(BaseModel):
    identity_id: Optional[uuid.UUID] = None
    credential_name: str
    credential_type: str
    vault_reference: str
    rotation_interval_days: int = 30
    policy_compliant: bool = True

class PAMCredentialLifecycleCreate(PAMCredentialLifecycleBase):
    pass

class PAMCredentialLifecycleResponse(PAMCredentialLifecycleBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: CredentialStatus
    last_rotated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Policies
# ─────────────────────────────────────────────────────────────────────────────
class PAMPolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    rules: Dict[str, Any] = Field(default_factory=dict)

class PAMPolicyCreate(PAMPolicyBase):
    pass

class PAMPolicyResponse(PAMPolicyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────────────────────
# Risk Scores
# ─────────────────────────────────────────────────────────────────────────────
class PAMRiskScoreBase(BaseModel):
    entity_type: str
    entity_id: str
    risk_score: float
    risk_level: PrivilegeRiskLevel
    contributing_factors: List[str] = Field(default_factory=list)

class PAMRiskScoreResponse(PAMRiskScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    evaluated_at: datetime
    class Config:
        from_attributes = True
