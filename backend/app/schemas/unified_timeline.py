import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

class UnifiedTimelineEventBase(BaseModel):
    timestamp: datetime
    source_module: str
    source_table: str
    source_id: str
    event_type: str
    event_summary: str
    render_metadata: Optional[Dict[str, Any]]

class EvidenceCorrelationBase(BaseModel):
    event_a_id: uuid.UUID
    event_b_id: uuid.UUID
    correlation_type: str
    correlation_value: str
    confidence_score: int

class UnifiedInvestigationBase(BaseModel):
    name: str

class UnifiedInvestigationCreate(UnifiedInvestigationBase):
    investigation_id: Optional[uuid.UUID] = None

class UnifiedInvestigationResponse(UnifiedInvestigationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    investigation_id: Optional[uuid.UUID]
    created_at: datetime
    
    events: List[UnifiedTimelineEventBase] = []
    correlations: List[EvidenceCorrelationBase] = []
    
    model_config = ConfigDict(from_attributes=True)
