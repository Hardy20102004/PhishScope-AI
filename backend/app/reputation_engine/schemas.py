from typing import Optional, List
from pydantic import ConfigDict, BaseModel
import uuid
from datetime import datetime

from app.reputation_engine.models import ReputationTrend

class EvidenceCreate(BaseModel):
    source: str
    description: str
    risk_delta: float = 0.0
    trust_delta: float = 0.0
    weight: float = 1.0

class EvidenceResponse(EvidenceCreate):
    id: uuid.UUID
    observed_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class HistoryResponse(BaseModel):
    id: uuid.UUID
    timestamp: datetime
    risk_score: float
    trust_score: float
    trigger_event: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class ProfileBase(BaseModel):
    entity_id: str
    entity_type: str

class ProfileResponse(ProfileBase):
    id: uuid.UUID
    risk_score: float
    trust_score: float
    confidence: float
    trend: ReputationTrend
    first_observed: datetime
    last_updated: datetime
    
    model_config = ConfigDict(from_attributes=True)

