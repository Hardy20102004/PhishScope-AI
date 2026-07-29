import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

# Chat Message
class CopilotChatMessageBase(BaseModel):
    role: str
    content: str
    evidence_citations: List[Dict[str, Any]] = []

class CopilotChatMessageCreate(BaseModel):
    content: str

class CopilotChatMessageResponse(CopilotChatMessageBase):
    id: uuid.UUID
    session_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Reasoning Log
class CopilotReasoningLogResponse(BaseModel):
    id: uuid.UUID
    observed_evidence: List[Dict[str, Any]]
    analytical_assessment: str
    confidence_score: float
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Session
class CopilotSessionBase(BaseModel):
    title: str
    context_tags: List[str] = []

class CopilotSessionCreate(CopilotSessionBase):
    pass

class CopilotSessionResponse(CopilotSessionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    messages: List[CopilotChatMessageResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
