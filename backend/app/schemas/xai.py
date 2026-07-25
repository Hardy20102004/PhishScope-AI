from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class ConfidenceFactor(BaseModel):
    factor: str
    impact: float
    description: str

class FeatureRank(BaseModel):
    feature_name: str
    rank: int
    category: str # e.g., "KNOWLEDGE_GRAPH", "POLICY", "OSINT"

class EvidenceAttributionBase(BaseModel):
    evidence_link_id: str
    importance_weight: float
    attribution_text: str
    source_type: Optional[str] = None # Enriched for UI
    source_id: Optional[str] = None # Enriched for UI

class ExplanationBase(BaseModel):
    decision_id: str
    executive_summary: str
    technical_summary: str
    confidence_breakdown: List[ConfidenceFactor] = []
    feature_importance: List[FeatureRank] = []

class ExplanationCreate(ExplanationBase):
    attributions: List[EvidenceAttributionBase] = []

class EvidenceAttributionResponse(EvidenceAttributionBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)

class ExplanationResponse(ExplanationBase):
    id: str
    created_at: datetime
    attributions: List[EvidenceAttributionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
