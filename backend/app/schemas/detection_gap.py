import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MitreCoverageMetricBase(BaseModel):
    tactic_id: str
    technique_id: str
    technique_name: str
    coverage_score: float

class MitreCoverageMetricResponse(MitreCoverageMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    evaluated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DetectionGapRecordBase(BaseModel):
    technique_id: str
    severity: str
    description: str
    is_remediated: bool

class DetectionGapRecordResponse(DetectionGapRecordBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ControlOptimizationPlanBase(BaseModel):
    gap_record_id: uuid.UUID
    title: str
    description: str
    target_platform: str
    expected_coverage_increase: float
    status: str

class ControlOptimizationPlanResponse(ControlOptimizationPlanBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
