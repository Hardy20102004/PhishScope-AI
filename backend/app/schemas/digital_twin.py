import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.models.digital_twin import (
    AssetNodeType, SimulationStatus, RiskLevel
)

# ─────────────────────────────────────────────────────────────────────────────
# Twin Assets
# ─────────────────────────────────────────────────────────────────────────────
class TwinAssetNodeBase(BaseModel):
    asset_name: str
    node_type: AssetNodeType
    attributes: Dict[str, Any] = Field(default_factory=dict)

class TwinAssetNodeResponse(TwinAssetNodeBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    last_synced_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Attack Paths
# ─────────────────────────────────────────────────────────────────────────────
class AttackPathGraphBase(BaseModel):
    title: str
    description: Optional[str] = None
    source_node_id: str
    target_node_id: str
    path_segments: List[Dict[str, Any]] = Field(default_factory=list)
    risk_level: RiskLevel
    is_simulated: bool = True

class AttackPathGraphResponse(AttackPathGraphBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    discovered_at: datetime
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Simulations
# ─────────────────────────────────────────────────────────────────────────────
class SimulationScenarioBase(BaseModel):
    name: str
    hypothesis: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class SimulationScenarioResponse(SimulationScenarioBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: SimulationStatus
    results: Dict[str, Any]
    created_at: datetime
    completed_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ─────────────────────────────────────────────────────────────────────────────
# Resilience Metrics
# ─────────────────────────────────────────────────────────────────────────────
class ResilienceMetricBase(BaseModel):
    domain: str
    score: float
    confidence_level: float
    contributing_factors: List[Dict[str, Any]] = Field(default_factory=list)

class ResilienceMetricResponse(ResilienceMetricBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    measured_at: datetime
    class Config:
        from_attributes = True
