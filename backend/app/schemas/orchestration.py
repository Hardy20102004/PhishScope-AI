import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.orchestration import (
    WorkflowType, WorkflowStatus, TaskStatus, AuthorizationStatus
)

# ─────────────────────────────────────────────────────────────────────────────
# Workflows
# ─────────────────────────────────────────────────────────────────────────────
class WorkflowRecordBase(BaseModel):
    workflow_type: WorkflowType
    name: str
    context_data: Dict[str, Any] = Field(default_factory=dict)

class WorkflowRecordCreate(WorkflowRecordBase):
    pass

class WorkflowRecordResponse(WorkflowRecordBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: WorkflowStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Playbooks
# ─────────────────────────────────────────────────────────────────────────────
class PlaybookDefinitionBase(BaseModel):
    name: str
    description: Optional[str] = None
    version: str = "1.0.0"
    requires_human_approval: bool = True
    steps: List[Dict[str, Any]] = Field(default_factory=list)

class PlaybookDefinitionResponse(PlaybookDefinitionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Tasks
# ─────────────────────────────────────────────────────────────────────────────
class TaskAssignmentBase(BaseModel):
    workflow_id: uuid.UUID
    title: str
    assigned_to: Optional[str] = None

class TaskAssignmentResponse(TaskAssignmentBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: TaskStatus
    created_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Decision Logs
# ─────────────────────────────────────────────────────────────────────────────
class DecisionLogBase(BaseModel):
    workflow_id: Optional[uuid.UUID] = None
    recommendation: str
    reasoning: Optional[str] = None

class DecisionLogResponse(DecisionLogBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    authorization_status: AuthorizationStatus
    authorized_by: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None
    class Config:
        from_attributes = True
