from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.base import APIResponse
from app.models.cyber_command import CommandStatus

class EnterpriseHealthMetricBase(BaseModel):
    domain: str
    health_score: float
    status: CommandStatus = CommandStatus.ACTIVE
    details: Dict[str, Any] = Field(default_factory=dict)

class EnterpriseHealthMetricCreate(EnterpriseHealthMetricBase):
    pass

class EnterpriseHealthMetric(EnterpriseHealthMetricBase):
    id: UUID
    evaluated_at: datetime

    class Config:
        orm_mode = True

class StrategicPlanBase(BaseModel):
    title: str
    description: str
    horizon: str
    milestones: List[Dict[str, Any]] = Field(default_factory=list)
    budget_allocation: Optional[float] = None

class StrategicPlanCreate(StrategicPlanBase):
    pass

class StrategicPlan(StrategicPlanBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ExecutiveCopilotSummaryBase(BaseModel):
    context_window: str
    observed_evidence: Dict[str, Any] = Field(default_factory=dict)
    calculated_metrics: Dict[str, Any] = Field(default_factory=dict)
    strategic_recommendations: List[str] = Field(default_factory=list)

class ExecutiveCopilotSummaryCreate(ExecutiveCopilotSummaryBase):
    pass

class ExecutiveCopilotSummary(ExecutiveCopilotSummaryBase):
    id: UUID
    generated_at: datetime

    class Config:
        orm_mode = True

class CyberCommandOverview(BaseModel):
    global_health_score: float
    active_operations_count: int
    critical_alerts: int
    strategic_alignment_score: float
    ai_strategic_briefing: str

class EnterpriseHealthMetricResponse(APIResponse[EnterpriseHealthMetric]):
    pass

class EnterpriseHealthMetricListResponse(APIResponse[List[EnterpriseHealthMetric]]):
    pass

class StrategicPlanResponse(APIResponse[StrategicPlan]):
    pass

class StrategicPlanListResponse(APIResponse[List[StrategicPlan]]):
    pass

class ExecutiveCopilotSummaryResponse(APIResponse[ExecutiveCopilotSummary]):
    pass

class ExecutiveCopilotSummaryListResponse(APIResponse[List[ExecutiveCopilotSummary]]):
    pass
