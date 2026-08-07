import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any

class GovernanceMetricBase(BaseModel):
    framework: str
    metric_name: str
    compliance_score: float

class GovernanceMetricResponse(GovernanceMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    measured_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BusinessImpactIndicatorBase(BaseModel):
    service_name: str
    criticality: str
    current_risk_score: float
    availability_status: str

class BusinessImpactIndicatorResponse(BusinessImpactIndicatorBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class InvestmentROIBase(BaseModel):
    initiative_name: str
    status: str
    hours_saved_monthly: float
    risk_reduction_percentage: float

class InvestmentROIResponse(InvestmentROIBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    evaluated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DecisionSupportBriefBase(BaseModel):
    title: str
    executive_summary: str
    recommendations: List[str]

class DecisionSupportBriefResponse(DecisionSupportBriefBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    generated_at: datetime
    model_config = ConfigDict(from_attributes=True)
