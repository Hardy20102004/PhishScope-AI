import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

class AlertEvidenceBase(BaseModel):
    evidence_type: str = Field(..., description="IP, DOMAIN, HASH, USER, HOST")
    value: str
    context: Optional[Dict[str, Any]] = None

class AlertEvidenceCreate(AlertEvidenceBase):
    pass

class AlertEvidenceResponse(AlertEvidenceBase):
    id: uuid.UUID
    alert_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AlertBase(BaseModel):
    title: str
    description: Optional[str] = None
    source: str = Field(..., description="EDR, SIEM, FIREWALL")
    source_alert_id: str
    category: str
    severity: str = Field(..., description="LOW, MEDIUM, HIGH, CRITICAL")
    tenant_id: uuid.UUID

class AlertCreate(AlertBase):
    mitre_techniques: Optional[Dict[str, Any]] = None
    evidence: Optional[List[AlertEvidenceCreate]] = None

class AlertUpdate(BaseModel):
    status: Optional[str] = None
    resolution_reason: Optional[str] = None
    priority_score: Optional[float] = None
    risk_score: Optional[float] = None
    confidence: Optional[float] = None
    ai_summary: Optional[str] = None

class AlertResponse(AlertBase):
    id: uuid.UUID
    status: str
    priority_score: float
    risk_score: float
    confidence: float
    mitre_techniques: Optional[Dict[str, Any]]
    ai_summary: Optional[str]
    resolution_reason: Optional[str]
    correlation_group_id: Optional[uuid.UUID]
    case_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
    
    evidence: List[AlertEvidenceResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class AlertLifecycleEventResponse(BaseModel):
    id: uuid.UUID
    alert_id: uuid.UUID
    user_id: Optional[uuid.UUID]
    previous_status: Optional[str]
    new_status: str
    comment: Optional[str]
    changed_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AlertAssignmentResponse(BaseModel):
    id: uuid.UUID
    alert_id: uuid.UUID
    user_id: uuid.UUID
    assigned_by: Optional[uuid.UUID]
    assigned_at: datetime
    active: bool
    
    model_config = ConfigDict(from_attributes=True)

class AlertAnalyticsDashboardResponse(BaseModel):
    active_alerts: int
    critical_alerts: int
    priority_distribution: Dict[str, int]
    source_distribution: Dict[str, int]
    mtta_minutes: float
    mttr_minutes: float


class AlertCorrelationGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    correlation_reason: str = Field(..., description="SHARED_IOC, THREAT_ACTOR, CAMPAIGN")

class AlertCorrelationGroupResponse(AlertCorrelationGroupBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    alerts: List[AlertResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
