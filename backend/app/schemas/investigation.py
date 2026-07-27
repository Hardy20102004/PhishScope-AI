from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import ConfigDict, BaseModel, Field

from app.models.investigation import InvestigationStatus, InvestigationType


class InvestigationCreate(BaseModel):
    target: str = Field(..., description="The URL, domain, IP, or hash to investigate")
    type: InvestigationType
    raw_content: Optional[str] = Field(None, description="Raw content or Base64 image payload")
    
class Finding(BaseModel):
    title: str
    description: str
    severity: str # LOW, MEDIUM, HIGH, CRITICAL

class InvestigationResponse(BaseModel):
    id: UUID
    target: str
    type: InvestigationType
    status: InvestigationStatus
    risk_score: Optional[int]
    risk_level: Optional[str]
    evidence: Dict[str, Any]
    findings: List[Finding]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)

