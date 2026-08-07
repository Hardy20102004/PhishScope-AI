from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.devsecops import PipelineStatus, GateStatus, SDLCPhase

# --- Pipeline Run ---
class PipelineRunBase(BaseModel):
    ci_provider: str
    run_identifier: str
    branch: str
    commit_sha: str
    status: PipelineStatus = PipelineStatus.QUEUED
    sdlc_phase: SDLCPhase = SDLCPhase.BUILD
    triggered_by: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class PipelineRunCreate(PipelineRunBase):
    repository_id: Optional[uuid.UUID] = None
    application_id: Optional[uuid.UUID] = None

class PipelineRunResponse(PipelineRunBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    repository_id: Optional[uuid.UUID]
    application_id: Optional[uuid.UUID]
    
    model_config = ConfigDict(from_attributes=True)

# --- Security Gate ---
class SecurityGateBase(BaseModel):
    gate_name: str
    gate_type: str
    status: GateStatus = GateStatus.PASS
    details: Dict[str, Any] = {}

class SecurityGateCreate(SecurityGateBase):
    pipeline_run_id: uuid.UUID

class SecurityGateResponse(SecurityGateBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    pipeline_run_id: uuid.UUID
    evaluated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- SDLC Workflow ---
class SDLCWorkflowBase(BaseModel):
    workflow_type: str
    status: str = "PENDING"
    requester: str
    approver: Optional[str] = None
    justification: Optional[str] = None

class SDLCWorkflowCreate(SDLCWorkflowBase):
    pipeline_run_id: Optional[uuid.UUID] = None
    application_id: Optional[uuid.UUID] = None

class SDLCWorkflowResponse(SDLCWorkflowBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    pipeline_run_id: Optional[uuid.UUID]
    application_id: Optional[uuid.UUID]
    created_at: datetime
    resolved_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

# --- Developer Metric ---
class DeveloperMetricBase(BaseModel):
    developer_email: str
    code_quality_score: float = 100.0
    security_score: float = 100.0
    vulnerabilities_introduced: int = 0
    vulnerabilities_fixed: int = 0
    training_completed: bool = False

class DeveloperMetricCreate(DeveloperMetricBase):
    pass

class DeveloperMetricResponse(DeveloperMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    last_calculated: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DevSecOpsExecutiveSummary(BaseModel):
    total_pipelines_run: int
    failed_security_gates: int
    open_exception_requests: int
    average_security_score: float
