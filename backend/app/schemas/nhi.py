import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.nhi import (
    MachineIdentityType, CredentialStatus, TrustType, RiskLevel
)

# ─────────────────────────────────────────────────────────────────────────────
# Machine Identity
# ─────────────────────────────────────────────────────────────────────────────
class NHIMachineIdentityBase(BaseModel):
    name: str
    identity_type: MachineIdentityType
    provider: str
    environment: str
    owner_id: Optional[str] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)

class NHIMachineIdentityCreate(NHIMachineIdentityBase):
    pass

class NHIMachineIdentityResponse(NHIMachineIdentityBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    credential_status: CredentialStatus
    last_rotated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Certificates
# ─────────────────────────────────────────────────────────────────────────────
class NHICertificateBase(BaseModel):
    common_name: str
    serial_number: str
    issuer: str
    valid_from: datetime
    valid_to: datetime
    identity_id: Optional[uuid.UUID] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)

class NHICertificateResponse(NHICertificateBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    is_revoked: bool
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Trust Relationships
# ─────────────────────────────────────────────────────────────────────────────
class NHITrustRelationshipBase(BaseModel):
    source_identity_id: uuid.UUID
    target_resource_arn: str
    trust_type: TrustType
    permissions: List[str] = Field(default_factory=list)

class NHITrustRelationshipResponse(NHITrustRelationshipBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Risk Score
# ─────────────────────────────────────────────────────────────────────────────
class NHIRiskScoreResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    identity_id: uuid.UUID
    overall_score: float
    over_permission_risk: float
    stale_credential_risk: float
    risk_level: RiskLevel
    evaluated_at: datetime
    class Config:
        from_attributes = True
