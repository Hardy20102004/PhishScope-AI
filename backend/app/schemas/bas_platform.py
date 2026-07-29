import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

class BasValidationResultBase(BaseModel):
    step_name: str
    expected_control: str
    was_detected: bool
    was_blocked: bool
    detection_reference: Optional[str]

class BasScenarioBase(BaseModel):
    name: str
    description: str
    tactic: str
    technique_id: str
    execution_steps: List[Dict[str, Any]]

class BasScenarioResponse(BasScenarioBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

class BasSimulationBase(BaseModel):
    scenario_id: uuid.UUID

class BasSimulationResponse(BasSimulationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    overall_score: float
    
    results: List[BasValidationResultBase] = []
    
    model_config = ConfigDict(from_attributes=True)
