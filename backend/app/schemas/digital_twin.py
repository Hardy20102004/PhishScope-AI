import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

# Recommendations
class OptimizationRecommendationBase(BaseModel):
    category: str
    title: str
    description: str
    expected_impact: str

class OptimizationRecommendationResponse(OptimizationRecommendationBase):
    id: uuid.UUID
    result_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

# Simulation Results
class SimulationResultBase(BaseModel):
    forecasted_mttr_mins: float
    forecasted_sla_breach_rate: float
    analyst_utilization_rate: float

class SimulationResultResponse(SimulationResultBase):
    id: uuid.UUID
    scenario_id: uuid.UUID
    simulated_at: datetime
    recommendations: List[OptimizationRecommendationResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# Simulation Scenarios
class SimulationScenarioBase(BaseModel):
    name: str
    description: str
    alert_volume_multiplier: float
    analyst_headcount: int
    automation_rate: float

class SimulationScenarioCreate(SimulationScenarioBase):
    pass

class SimulationScenarioResponse(SimulationScenarioBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    
    results: List[SimulationResultResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
