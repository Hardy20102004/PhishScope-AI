import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class StrategicForecastBase(BaseModel):
    metric_name: str
    target_date: datetime
    projected_value: float
    confidence_score: float

class StrategicForecastResponse(StrategicForecastBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    generated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class OptimizationRoadmapBase(BaseModel):
    title: str
    nist_function: str
    status: str
    start_date: datetime
    target_end_date: datetime

class OptimizationRoadmapResponse(OptimizationRoadmapBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class StrategicRecommendationBase(BaseModel):
    title: str
    description: str
    expected_impact: str
    status: str

class StrategicRecommendationResponse(StrategicRecommendationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    generated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DecisionApprovalLogBase(BaseModel):
    recommendation_id: uuid.UUID
    executive_user_id: uuid.UUID
    action_taken: str
    justification: Optional[str] = None

class DecisionApprovalLogResponse(DecisionApprovalLogBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
