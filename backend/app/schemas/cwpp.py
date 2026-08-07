import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class CloudWorkloadBase(BaseModel):
    workload_type: str
    workload_name: str
    provider: str
    region: str
    status: str
    criticality: str

class CloudWorkloadResponse(CloudWorkloadBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RuntimeEventBase(BaseModel):
    workload_id: uuid.UUID
    event_type: str
    process_name: Optional[str] = None
    command_line: Optional[str] = None
    destination_ip: Optional[str] = None

class RuntimeEventResponse(RuntimeEventBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class BehaviorAnomalyBase(BaseModel):
    workload_id: uuid.UUID
    event_id: Optional[uuid.UUID] = None
    title: str
    severity: str
    description: str

class BehaviorAnomalyResponse(BehaviorAnomalyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    detected_at: datetime
    model_config = ConfigDict(from_attributes=True)

class WorkloadRiskScoreBase(BaseModel):
    workload_id: uuid.UUID
    risk_score: float

class WorkloadRiskScoreResponse(WorkloadRiskScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
