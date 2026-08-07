import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import UUID4, BaseModel, Field, field_validator, ConfigDict

from app.models.multi_agent import (
    AgentHealth,
    AgentStatus,
    ApprovalStatus,
    MessageType,
    TaskStatus,
)


# Agent Definition Schemas
class AgentDefinitionBase(BaseModel):
    agent_name: str
    description: Optional[str] = None
    capabilities_json: List[str] = Field(default_factory=list)
    supported_tasks_json: List[str] = Field(default_factory=list)
    version: str = "1.0.0"
    dependencies_json: List[str] = Field(default_factory=list)
    owner: str = "System"
    preferred_capability: Optional[str] = None

class AgentDefinitionCreate(AgentDefinitionBase):
    pass

class AgentDefinitionResponse(AgentDefinitionBase):
    id: UUID4
    status: AgentStatus
    health: AgentHealth
    created_at: datetime
    updated_at: datetime

# Task Schemas
class AgentTaskBase(BaseModel):
    parent_id: Optional[UUID4] = None
    investigation_id: Optional[UUID4] = None
    case_id: Optional[UUID4] = None
    session_id: Optional[str] = None
    task_name: str
    assigned_agent_id: str
    input_payload_json: Dict[str, Any] = Field(default_factory=dict)
    dependency_task_ids_json: List[str] = Field(default_factory=list)

class AgentTaskCreate(AgentTaskBase):
    pass

class AgentTaskResponse(AgentTaskBase):
    id: UUID4
    status: TaskStatus
    output_findings_json: Dict[str, Any]
    retry_count: int
    confidence_score: Optional[float] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    updated_at: datetime

# Plan Orchestration Schemas
class PlanRequest(BaseModel):
    objective: str
    case_id: Optional[UUID4] = None
    investigation_id: Optional[UUID4] = None
    context_artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    require_human_approval_threshold: float = 0.70

class PlanResponse(BaseModel):
    plan_id: str
    tasks: List[AgentTaskResponse]
    estimated_duration_seconds: int
    agents_involved: List[str]

# Communication Schemas
class AgentMessageCreate(BaseModel):
    sender_id: str
    receiver_id: Optional[str] = None
    message_type: MessageType
    content_json: Dict[str, Any]
    correlation_id: Optional[str] = None

class AgentMessageResponse(AgentMessageCreate):
    id: UUID4
    created_at: datetime

# Human Approval Schemas
class HumanApprovalSubmit(BaseModel):
    status: ApprovalStatus
    reviewer_user_id: UUID4
    reviewer_feedback: Optional[str] = None

class HumanApprovalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    task_id: UUID4
    requesting_agent_id: str
    description: str
    risk_severity: str
    status: ApprovalStatus
    reviewer_user_id: Optional[UUID4] = None
    reviewer_feedback: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    @field_validator('reviewer_user_id', mode='before')
    @classmethod
    def coerce_reviewer_uuid(cls, v):
        if isinstance(v, str):
            return uuid.UUID(v)
        return v
