import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

# Evidence
class HuntEvidenceBase(BaseModel):
    evidence_type: str = Field(..., description="ALERT, IOC, GRAPH_NODE, EVENT")
    reference_id: str
    notes: Optional[str] = None
    is_key_finding: bool = False

class HuntEvidenceCreate(HuntEvidenceBase):
    pass

class HuntEvidenceResponse(HuntEvidenceBase):
    id: uuid.UUID
    session_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Hypothesis
class HuntHypothesisBase(BaseModel):
    hypothesis_text: str
    is_ai_generated: bool = True
    confidence_score: float = 0.0
    mitre_tactics: Optional[Dict[str, Any]] = None
    mitre_techniques: Optional[Dict[str, Any]] = None
    suggested_queries: List[str] = []
    status: str = "PROPOSED"

class HuntHypothesisCreate(HuntHypothesisBase):
    pass

class HuntHypothesisResponse(HuntHypothesisBase):
    id: uuid.UUID
    session_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Query
class HuntQueryBase(BaseModel):
    query_type: str = "NATURAL_LANGUAGE"
    raw_query: str

class HuntQueryCreate(HuntQueryBase):
    pass

class HuntQueryResponse(HuntQueryBase):
    id: uuid.UUID
    session_id: uuid.UUID
    translated_structured_query: Optional[Dict[str, Any]] = None
    results_count: int
    execution_time_ms: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Session
class HuntSessionBase(BaseModel):
    title: str
    objective: Optional[str] = None
    status: str = "ACTIVE"

class HuntSessionCreate(HuntSessionBase):
    pass

class HuntSessionUpdate(BaseModel):
    title: Optional[str] = None
    objective: Optional[str] = None
    status: Optional[str] = None

class HuntSessionResponse(HuntSessionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    assigned_hunter_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
    
    # Optionally include lists if needed, but usually kept flat for list endpoints
    queries: List[HuntQueryResponse] = []
    hypotheses: List[HuntHypothesisResponse] = []
    evidence: List[HuntEvidenceResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
