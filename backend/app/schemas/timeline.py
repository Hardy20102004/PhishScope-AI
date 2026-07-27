from typing import Optional, List, Dict, Any
from pydantic import ConfigDict, BaseModel, Field
from datetime import datetime
from app.models.timeline import TimelineType, EventCategory

class EventEvidenceBase(BaseModel):
    source_type: str
    reference_url: Optional[str] = None
    snippet: Optional[str] = None

class EventEvidenceCreate(EventEvidenceBase):
    pass

class EventEvidenceResponse(EventEvidenceBase):
    id: str
    event_id: str
    
    model_config = ConfigDict(from_attributes=True)

class ThreatTimelineEventBase(BaseModel):
    timestamp: datetime
    title: str
    description: Optional[str] = None
    category: EventCategory = EventCategory.OBSERVATION
    entity_id: Optional[str] = None
    confidence: float = 1.0
    is_hypothetical: bool = False
    properties_json: Dict[str, Any] = Field(default_factory=dict)

class ThreatTimelineEventCreate(ThreatTimelineEventBase):
    evidence: Optional[List[EventEvidenceCreate]] = None

class ThreatTimelineEventResponse(ThreatTimelineEventBase):
    id: str
    timeline_id: str
    created_at: datetime
    evidence: List[EventEvidenceResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class TimelineBase(BaseModel):
    name: str
    description: Optional[str] = None
    timeline_type: TimelineType
    tenant_id: Optional[str] = None

class TimelineCreate(TimelineBase):
    pass

class TimelineResponse(TimelineBase):
    id: str
    created_at: datetime
    updated_at: datetime
    events: List[ThreatTimelineEventResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

