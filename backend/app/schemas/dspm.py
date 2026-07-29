import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class CloudDataAssetBase(BaseModel):
    asset_name: str
    provider: str
    service_type: str
    location: str
    is_public: bool
    is_encrypted: bool
    encryption_type: Optional[str] = None

class CloudDataAssetResponse(CloudDataAssetBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DataClassificationBase(BaseModel):
    asset_id: uuid.UUID
    label: str
    confidence_score: float
    requires_review: bool

class DataClassificationResponse(DataClassificationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    classified_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DataExposureFindingBase(BaseModel):
    asset_id: uuid.UUID
    finding_type: str
    severity: str
    description: str
    status: str

class DataExposureFindingResponse(DataExposureFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    detected_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DataAccessGovernanceBase(BaseModel):
    asset_id: uuid.UUID
    principal_id: str
    access_level: str
    is_dormant: bool
    last_accessed: Optional[datetime] = None

class DataAccessGovernanceResponse(DataAccessGovernanceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    analyzed_at: datetime
    model_config = ConfigDict(from_attributes=True)
