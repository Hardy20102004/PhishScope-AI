from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class ThreatFeedResultBase(BaseModel):
    source: str
    reputation_score: float
    confidence: float
    threat_classification: Optional[str] = None
    is_cached: bool = False
    created_at: datetime
    
class ThreatFeedResultResponse(ThreatFeedResultBase):
    id: UUID
    indicator_id: UUID
    raw_data: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class IndicatorBase(BaseModel):
    value: str
    type: str
    normalized_value: str

class IndicatorCreate(IndicatorBase):
    pass

class IndicatorResponse(IndicatorBase):
    id: UUID
    reputation_score: float
    confidence_score: float
    threat_classification: Optional[str] = None
    first_seen: datetime
    last_seen: datetime
    last_updated: datetime
    observation_count: int
    
    feed_results: List[ThreatFeedResultResponse] = []

    model_config = ConfigDict(from_attributes=True)

class IndicatorSearchRequest(BaseModel):
    value: str

class IndicatorCorrelationBase(BaseModel):
    source_indicator_id: UUID
    target_indicator_id: UUID
    correlation_type: str
    confidence: float
    created_at: datetime

class IndicatorCorrelationResponse(IndicatorCorrelationBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
