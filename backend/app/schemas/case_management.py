from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.case_management import CasePriority, CaseStatus, TaskStatus


class CaseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: CasePriority = CasePriority.MEDIUM
    tags: List[str] = []

class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CasePriority] = None
    tags: Optional[List[str]] = None

class CaseTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: Optional[UUID] = None

class CaseTaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None

class CaseTaskSchema(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    assignee_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TimelineEventSchema(BaseModel):
    id: UUID
    action: str
    details: Optional[str]
    metadata_json: dict
    created_at: datetime
    user_id: Optional[UUID]
    
    model_config = ConfigDict(from_attributes=True)

class DecisionLogCreate(BaseModel):
    decision: str
    reasoning: str
    confidence_score: int
    evidence_references: List[dict] = []

class DecisionLogSchema(BaseModel):
    id: UUID
    decision: str
    reasoning: str
    confidence_score: int
    evidence_references: List[dict]
    created_at: datetime
    user_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class CaseSchema(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: CaseStatus
    priority: CasePriority
    tags: List[str]
    owner_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    tasks: List[CaseTaskSchema] = []
    
    model_config = ConfigDict(from_attributes=True)
