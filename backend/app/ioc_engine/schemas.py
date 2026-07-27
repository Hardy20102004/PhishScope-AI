from typing import Optional, List, Dict, Any
from pydantic import ConfigDict, BaseModel, Field
import uuid
from datetime import datetime

from app.models.threat_intel import IOCType, RelationshipType

class IndicatorBase(BaseModel):
    value: str = Field(..., description="The raw value of the indicator")
    type: IOCType = Field(..., description="The type of the IOC")
    normalized_value: str = Field(..., description="Canonical value of the indicator")
    source_module: Optional[str] = Field(None, description="Module that discovered the IOC")
    raw_context: Optional[Dict[str, Any]] = Field(None, description="Raw context of discovery")
    normalization_metadata: Optional[Dict[str, Any]] = Field(None)
    
    reputation_score: float = Field(0.0)
    confidence_score: float = Field(0.0)
    threat_classification: Optional[str] = Field(None)

class IndicatorCreate(IndicatorBase):
    pass

class IndicatorResponse(IndicatorBase):
    id: uuid.UUID
    first_seen: datetime
    last_seen: datetime
    last_updated: datetime
    observation_count: int

    model_config = ConfigDict(from_attributes=True)

class IndicatorCorrelationBase(BaseModel):
    source_indicator_id: uuid.UUID
    target_indicator_id: uuid.UUID
    correlation_type: str
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    similarity_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class IndicatorCorrelationCreate(IndicatorCorrelationBase):
    pass

class IndicatorCorrelationResponse(IndicatorCorrelationBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CorrelationEvidenceBase(BaseModel):
    relationship_id: uuid.UUID
    evidence_type: str
    description: str
    evidence_data: Optional[Dict[str, Any]] = None
    source_system: Optional[str] = None

class CorrelationEvidenceCreate(CorrelationEvidenceBase):
    pass

class CorrelationEvidenceResponse(CorrelationEvidenceBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class IndicatorRiskBase(BaseModel):
    indicator_id: uuid.UUID
    risk_score: float = Field(0.0, ge=0.0, le=100.0)
    confidence_level: float = Field(0.0, ge=0.0, le=1.0)
    uncertainty: float = Field(0.0, ge=0.0, le=1.0)
    priority: int = 0
    threat_actor: Optional[str] = None
    campaign: Optional[str] = None

class IndicatorRiskResponse(IndicatorRiskBase):
    id: uuid.UUID
    calculated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CorrelationAnalytics(BaseModel):
    total_indicators: int
    total_relationships: int
    average_confidence: float
    top_ioc_types: Dict[str, int]
    top_threat_actors: List[str]
    emerging_indicators: List[IndicatorResponse]
