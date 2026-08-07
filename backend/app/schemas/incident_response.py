import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

# Chain of Custody
class ChainOfCustodyLogBase(BaseModel):
    action: str
    digital_signature: str
    notes: Optional[str] = None

class ChainOfCustodyLogResponse(ChainOfCustodyLogBase):
    id: uuid.UUID
    evidence_id: uuid.UUID
    performed_by_id: Optional[uuid.UUID]
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Evidence
class EvidenceRecordBase(BaseModel):
    artifact_type: str
    artifact_value: str
    source: str

class EvidenceRecordCreate(EvidenceRecordBase):
    pass

class EvidenceRecordResponse(EvidenceRecordBase):
    id: uuid.UUID
    case_id: uuid.UUID
    created_at: datetime
    chain_of_custody: List[ChainOfCustodyLogResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Task
class IncidentTaskBase(BaseModel):
    title: str
    task_type: str
    status: str = "TODO"

class IncidentTaskCreate(IncidentTaskBase):
    pass

class IncidentTaskResponse(IncidentTaskBase):
    id: uuid.UUID
    incident_id: uuid.UUID
    assigned_to_id: Optional[uuid.UUID]
    created_at: datetime
    due_date: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

# Case
class DFIRCaseBase(BaseModel):
    title: str
    case_type: str
    status: str = "OPEN"

class DFIRCaseCreate(DFIRCaseBase):
    pass

class DFIRCaseResponse(DFIRCaseBase):
    id: uuid.UUID
    incident_id: uuid.UUID
    created_at: datetime
    evidence: List[EvidenceRecordResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Incident
class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str = "MEDIUM"
    status: str = "NEW"

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None

class IncidentResponse(IncidentBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    lead_investigator_id: Optional[uuid.UUID]
    created_at: datetime
    resolved_at: Optional[datetime]
    
    cases: List[DFIRCaseResponse] = []
    tasks: List[IncidentTaskResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
