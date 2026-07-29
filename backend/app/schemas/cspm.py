import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Dict, Any

class CloudAssetBase(BaseModel):
    provider: str
    asset_type: str
    asset_name: str
    region: str
    configuration: Dict[str, Any]

class CloudAssetResponse(CloudAssetBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CloudMisconfigurationBase(BaseModel):
    asset_id: uuid.UUID
    title: str
    severity: str
    description: str
    remediation_steps: str
    status: str

class CloudMisconfigurationResponse(CloudMisconfigurationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    detected_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ComplianceFindingBase(BaseModel):
    framework: str
    control_id: str
    passed: int
    failed: int

class ComplianceFindingResponse(ComplianceFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    evaluated_at: datetime
    model_config = ConfigDict(from_attributes=True)
