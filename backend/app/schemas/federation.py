import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.federation import (
    FederationRole, ProtocolType, TrustStatus, RiskLevel
)

# ─────────────────────────────────────────────────────────────────────────────
# Providers
# ─────────────────────────────────────────────────────────────────────────────
class FederatedProviderBase(BaseModel):
    name: str
    role: FederationRole
    entity_id: str
    business_owner: Optional[str] = None
    environment: str = "Production"

class FederatedProviderCreate(FederatedProviderBase):
    pass

class FederatedProviderResponse(FederatedProviderBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Trusts
# ─────────────────────────────────────────────────────────────────────────────
class FederationTrustBase(BaseModel):
    idp_id: uuid.UUID
    sp_id: uuid.UUID
    protocol: ProtocolType
    status: TrustStatus = TrustStatus.ACTIVE
    attribute_mapping: Dict[str, Any] = Field(default_factory=dict)

class FederationTrustCreate(FederationTrustBase):
    pass

class FederationTrustResponse(FederationTrustBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    established_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Config & Metadata
# ─────────────────────────────────────────────────────────────────────────────
class FederationProtocolConfigResponse(BaseModel):
    id: uuid.UUID
    trust_id: uuid.UUID
    requires_signed_assertions: bool
    requires_encrypted_assertions: bool
    allowed_redirect_uris: List[str]
    metadata_url: Optional[str]
    class Config:
        from_attributes = True

class FederationCertificateResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    provider_id: uuid.UUID
    common_name: str
    thumbprint: str
    valid_from: datetime
    valid_to: datetime
    is_active: bool
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Risk
# ─────────────────────────────────────────────────────────────────────────────
class FederationRiskScoreResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    trust_id: uuid.UUID
    overall_score: float
    protocol_risk: float
    certificate_risk: float
    risk_level: RiskLevel
    evaluated_at: datetime
    class Config:
        from_attributes = True
