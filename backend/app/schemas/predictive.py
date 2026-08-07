from typing import Optional, List, Dict, Any
from pydantic import ConfigDict, BaseModel, Field
from datetime import datetime
from app.models.predictive import ForecastDomain, ForecastStatus

class ForecastEvidenceBase(BaseModel):
    evidence_type: str
    reference_id: str
    explanation: Optional[str] = None

class ForecastEvidenceCreate(ForecastEvidenceBase):
    pass

class ForecastEvidenceResponse(ForecastEvidenceBase):
    id: str
    forecast_id: str
    
    model_config = ConfigDict(from_attributes=True)

class ForecastScenarioBase(BaseModel):
    scenario_name: str
    description: str
    probability: float

class ForecastScenarioCreate(ForecastScenarioBase):
    pass

class ForecastScenarioResponse(ForecastScenarioBase):
    id: str
    forecast_id: str
    
    model_config = ConfigDict(from_attributes=True)

class ThreatForecastBase(BaseModel):
    title: str
    description: str
    domain: ForecastDomain
    tenant_id: Optional[str] = None
    confidence_score: float = 0.5
    uncertainty_score: float = 0.5
    time_horizon_start: Optional[datetime] = None
    time_horizon_end: Optional[datetime] = None
    properties_json: Dict[str, Any] = Field(default_factory=dict)

class ThreatForecastCreate(ThreatForecastBase):
    scenarios: Optional[List[ForecastScenarioCreate]] = None
    evidence: Optional[List[ForecastEvidenceCreate]] = None

class ThreatForecastResponse(ThreatForecastBase):
    id: str
    status: ForecastStatus
    created_at: datetime
    updated_at: datetime
    scenarios: List[ForecastScenarioResponse] = []
    evidence: List[ForecastEvidenceResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

