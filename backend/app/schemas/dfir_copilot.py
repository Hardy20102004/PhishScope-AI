import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict
from app.models.copilot import MessageRole

class DfirResponseChunk(BaseModel):
    content: str
    classification: str # OBSERVATION, ASSESSMENT, RECOMMENDATION, UNKNOWN
    citations: List[Dict[str, str]] = [] # e.g. [{"id": "uuid", "type": "DISK_MFT"}]

class DfirQuery(BaseModel):
    conversation_id: uuid.UUID
    content: str
    investigation_id: uuid.UUID
    context_type: str = "TIMELINE" # TIMELINE, ARTIFACT, GENERAL

class DfirResponse(BaseModel):
    message_id: uuid.UUID
    chunks: List[DfirResponseChunk]
    suggested_questions: List[str] = []
