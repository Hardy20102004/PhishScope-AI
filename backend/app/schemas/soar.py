import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

# Approval
class ApprovalRecordBase(BaseModel):
    step_id: str
    action_requested: str
    status: str = "PENDING"
    review_notes: Optional[str] = None

class ApprovalRecordResponse(ApprovalRecordBase):
    id: uuid.UUID
    execution_id: uuid.UUID
    reviewed_by_id: Optional[uuid.UUID]
    requested_at: datetime
    reviewed_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

class ApprovalReview(BaseModel):
    approved: bool
    notes: Optional[str] = None

# Execution
class ExecutionHistoryBase(BaseModel):
    status: str = "RUNNING"
    current_step_id: Optional[str] = None

class ExecutionHistoryCreate(BaseModel):
    incident_id: Optional[uuid.UUID] = None

class ExecutionHistoryResponse(ExecutionHistoryBase):
    id: uuid.UUID
    playbook_id: uuid.UUID
    incident_id: Optional[uuid.UUID]
    execution_log: List[Dict[str, Any]] = []
    started_at: datetime
    completed_at: Optional[datetime]
    approvals: List[ApprovalRecordResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Playbook
class PlaybookBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "DRAFT"
    workflow_data: Dict[str, Any] = {}

class PlaybookCreate(PlaybookBase):
    pass

class PlaybookUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    workflow_data: Optional[Dict[str, Any]] = None

class PlaybookResponse(PlaybookBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    version: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
