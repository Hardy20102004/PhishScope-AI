import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional

class CloudTelemetryEventBase(BaseModel):
    provider: str
    event_source: str
    event_name: str
    principal_id: Optional[str] = None
    resource_id: Optional[str] = None
    source_ip: Optional[str] = None
    raw_data: Dict[str, Any]

class CloudTelemetryEventResponse(CloudTelemetryEventBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class CloudDetectionBase(BaseModel):
    investigation_id: Optional[uuid.UUID] = None
    rule_name: str
    severity: str
    description: str
    mitre_tactics: List[str]
    evidence_events: List[str]

class CloudDetectionResponse(CloudDetectionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    detected_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CloudInvestigationBase(BaseModel):
    title: str
    status: str
    priority: str
    primary_entity: str

class CloudInvestigationResponse(CloudInvestigationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ResponseActionBase(BaseModel):
    investigation_id: uuid.UUID
    action_type: str
    target_entity: str
    description: str
    status: str

class ResponseActionResponse(ResponseActionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    approver_id: Optional[uuid.UUID] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
