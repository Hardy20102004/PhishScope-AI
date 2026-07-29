import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

class ReadinessSnapshotBase(BaseModel):
    overall_maturity_score: float
    detection_health_score: float
    analyst_readiness_score: float
    aggregated_metrics: Dict[str, Any]

class ReadinessSnapshotResponse(ReadinessSnapshotBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class DetectionMetricBase(BaseModel):
    rule_name: str
    rule_id: str
    data_source: str
    total_alerts: int
    false_positives: int
    true_positives: int
    status: str

class DetectionMetricResponse(DetectionMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    last_evaluated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AnalystTeamMetricBase(BaseModel):
    team_name: str
    evaluation_period: str
    mean_time_to_triage_mins: float
    mean_time_to_resolve_mins: float
    playbook_adherence_percent: float

class AnalystTeamMetricResponse(AnalystTeamMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
