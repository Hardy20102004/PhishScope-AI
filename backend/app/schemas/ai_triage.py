import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

class AnalystFeedbackBase(BaseModel):
    feedback_type: str = Field(..., description="FALSE_POSITIVE, TRUE_POSITIVE, PRIORITY_OVERRIDE, BAD_RECOMMENDATION")
    priority_override: Optional[str] = None
    comments: Optional[str] = None

class AnalystFeedbackCreate(AnalystFeedbackBase):
    pass

class AnalystFeedbackResponse(AnalystFeedbackBase):
    id: uuid.UUID
    triage_group_id: uuid.UUID
    user_id: Optional[uuid.UUID]
    processed_by_learning_engine: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AlertRecommendationBase(BaseModel):
    alert_summary: str
    priority_explanation: str
    business_impact_summary: str
    investigation_steps: List[str]
    alternative_interpretations: List[str]
    ai_confidence_score: float
    uncertainty_factors: List[str]

class AlertRecommendationResponse(AlertRecommendationBase):
    id: uuid.UUID
    triage_group_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AITriageGroupBase(BaseModel):
    name: str
    grouping_reason: str
    confidence: float
    overall_priority_score: float
    business_impact_score: float
    priority_tier: str
    status: str

class AITriageGroupResponse(AITriageGroupBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    recommendation: Optional[AlertRecommendationResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

class AssetBusinessContextBase(BaseModel):
    asset_identifier: str
    criticality_score: float
    business_service: Optional[str] = None
    data_sensitivity: str

class AssetBusinessContextCreate(AssetBusinessContextBase):
    pass

class AssetBusinessContextResponse(AssetBusinessContextBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
