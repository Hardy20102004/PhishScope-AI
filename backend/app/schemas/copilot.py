from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.copilot import CopilotSessionStatus, CodeReviewStatus

# --- Copilot Session ---
class DeveloperCopilotSessionBase(BaseModel):
    repository_context: Optional[str] = None
    environment: str = "VS_CODE"
    status: CopilotSessionStatus = CopilotSessionStatus.ACTIVE

class DeveloperCopilotSessionCreate(DeveloperCopilotSessionBase):
    pass

class DeveloperCopilotSessionResponse(DeveloperCopilotSessionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    developer_id: uuid.UUID
    created_at: datetime
    last_activity_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Code Review Record ---
class CodeReviewRecordBase(BaseModel):
    repository_url: str
    pull_request_id: Optional[str] = None
    commit_hash: Optional[str] = None

class CodeReviewRecordCreate(CodeReviewRecordBase):
    pass

class CodeReviewRecordResponse(CodeReviewRecordBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: CodeReviewStatus
    findings_count: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# --- Code Review Finding ---
class CodeReviewFindingBase(BaseModel):
    file_path: str
    line_number: Optional[int] = None
    severity: str = "MEDIUM"
    cwe_id: Optional[str] = None
    description: str
    suggestion: str

class CodeReviewFindingCreate(CodeReviewFindingBase):
    review_id: uuid.UUID

class CodeReviewFindingResponse(CodeReviewFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    review_id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

# --- Developer Learning Progress ---
class DeveloperLearningProgressBase(BaseModel):
    topic: str
    modules_completed: int = 0

class DeveloperLearningProgressCreate(DeveloperLearningProgressBase):
    pass

class DeveloperLearningProgressResponse(DeveloperLearningProgressBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    developer_id: uuid.UUID
    last_engaged_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Engineering Intelligence ---
class EngineeringMetricBase(BaseModel):
    project_name: str
    technical_debt_score: float = 0.0
    security_trend_score: float = 0.0

class EngineeringMetricCreate(EngineeringMetricBase):
    pass

class EngineeringMetricResponse(EngineeringMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    calculated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Legacy SOC Copilot Schemas ---
class ChatMessageRequest(BaseModel):
    content: str

class CopilotMessageSchema(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    evidence_references: List[dict] = []
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class RecommendationsResponse(BaseModel):
    recommendations: List[str]

class ReportRequest(BaseModel):
    report_type: str = "Executive"

class GeneratedReportSchema(BaseModel):
    id: uuid.UUID
    report_type: str
    content: str
    generated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

