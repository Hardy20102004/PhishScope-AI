from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.secrets import SecretType, SecretLifecycleStatus

# --- Secret Metadata ---
class SecretMetadataBase(BaseModel):
    secret_type: SecretType = SecretType.UNKNOWN
    name: str
    identifier_hash: Optional[str] = None
    location_uri: str
    lifecycle_status: SecretLifecycleStatus = SecretLifecycleStatus.ACTIVE
    expires_at: Optional[datetime] = None
    last_rotated_at: Optional[datetime] = None
    owner: Optional[str] = None

class SecretMetadataCreate(SecretMetadataBase):
    pass

class SecretMetadataResponse(SecretMetadataBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Secret Exposure ---
class SecretExposureBase(BaseModel):
    exposure_type: str
    severity: str = "HIGH"
    details: str

class SecretExposureCreate(SecretExposureBase):
    secret_id: uuid.UUID

class SecretExposureResponse(SecretExposureBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    secret_id: uuid.UUID
    detected_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Secret Policy ---
class SecretPolicyBase(BaseModel):
    name: str
    description: str
    target_secret_type: SecretType = SecretType.UNKNOWN
    max_age_days: int = 90
    is_active: bool = True

class SecretPolicyCreate(SecretPolicyBase):
    pass

class SecretPolicyResponse(SecretPolicyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

# --- Secret Guidance ---
class SecretGuidanceBase(BaseModel):
    remediation_steps: str

class SecretGuidanceCreate(SecretGuidanceBase):
    exposure_id: uuid.UUID

class SecretGuidanceResponse(SecretGuidanceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    exposure_id: uuid.UUID
    generated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Executive Summary ---
class SecretsExecutiveSummary(BaseModel):
    total_active_secrets: int
    total_exposures: int
    expiring_certificates_30d: int
    dormant_credentials: int
