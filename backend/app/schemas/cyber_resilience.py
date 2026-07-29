import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CyberResilienceScoreBase(BaseModel):
    overall_score: float
    preventive_effectiveness: float
    detective_effectiveness: float
    response_effectiveness: float

class CyberResilienceScoreResponse(CyberResilienceScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    calculated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MaturityAssessmentBase(BaseModel):
    domain: str
    maturity_tier: int
    justification: str

class MaturityAssessmentResponse(MaturityAssessmentBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    assessed_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ExecutiveKPIBase(BaseModel):
    metric_name: str
    metric_value: float
    metric_unit: str
    trend: str

class ExecutiveKPIResponse(ExecutiveKPIBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    measured_at: datetime
    model_config = ConfigDict(from_attributes=True)
