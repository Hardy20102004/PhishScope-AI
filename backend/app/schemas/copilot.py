from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ChatMessageRequest(BaseModel):
    content: str

class CopilotMessageSchema(BaseModel):
    id: UUID
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
    id: UUID
    report_type: str
    content: str
    generated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
