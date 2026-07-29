import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional

class UnifiedCloudAssetBase(BaseModel):
    asset_name: str
    provider: str
    asset_type: str
    environment: str
    native_id: str
    tags: Dict[str, str]

class UnifiedCloudAssetResponse(UnifiedCloudAssetBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    last_seen: datetime
    model_config = ConfigDict(from_attributes=True)

class CrossCloudRelationshipBase(BaseModel):
    source_asset_id: uuid.UUID
    target_asset_id: uuid.UUID
    relationship_type: str

class CrossCloudRelationshipResponse(CrossCloudRelationshipBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UnifiedRiskScoreBase(BaseModel):
    global_score: float
    provider_breakdown: Dict[str, float]
    category_breakdown: Dict[str, float]

class UnifiedRiskScoreResponse(UnifiedRiskScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    calculated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ComplianceTrendBase(BaseModel):
    framework: str
    compliance_percentage: float
    failed_controls: int

class ComplianceTrendResponse(ComplianceTrendBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    recorded_at: datetime
    model_config = ConfigDict(from_attributes=True)
