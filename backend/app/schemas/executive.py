import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

# Executive Metric
class ExecutiveMetricBase(BaseModel):
    metric_name: str
    metric_value: float
    timestamp: datetime

class ExecutiveMetricResponse(ExecutiveMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

# Business Risk
class BusinessRiskScoreBase(BaseModel):
    business_unit: str
    risk_score: int
    factors: Dict[str, Any] = {}
    timestamp: datetime

class BusinessRiskScoreResponse(BusinessRiskScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

# Executive Report
class ExecutiveReportBase(BaseModel):
    report_type: str
    title: str
    content: str

class ExecutiveReportResponse(ExecutiveReportBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
