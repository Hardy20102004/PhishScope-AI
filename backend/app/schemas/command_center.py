import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional

class EnterpriseCloudMetricBase(BaseModel):
    metric_type: str
    metric_value: float
    metric_trend: str

class EnterpriseCloudMetricResponse(EnterpriseCloudMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    calculated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class OperationalMetricBase(BaseModel):
    metric_name: str
    metric_value: float

class OperationalMetricResponse(OperationalMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    measured_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CommandCenterAuditLogBase(BaseModel):
    action_type: str
    target_resource: str
    actor_id: uuid.UUID
    justification: str

class CommandCenterAuditLogResponse(CommandCenterAuditLogBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
