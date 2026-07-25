from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.automation import ExecutionStatus, TriggerType


class WorkflowVersionBase(BaseModel):
    version_number: int
    definition_json: dict
    created_at: datetime
    created_by: Optional[UUID]

    model_config = ConfigDict(from_attributes=True)

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    trigger_type: TriggerType
    is_active: bool = False

class WorkflowCreate(WorkflowBase):
    definition_json: dict

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_type: Optional[TriggerType] = None
    is_active: Optional[bool] = None

class WorkflowSchema(WorkflowBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    versions: List[WorkflowVersionBase] = []

    model_config = ConfigDict(from_attributes=True)

class WorkflowExecutionSchema(BaseModel):
    id: UUID
    version_id: UUID
    trigger_event_json: dict
    status: ExecutionStatus
    logs_json: list
    started_at: datetime
    completed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
