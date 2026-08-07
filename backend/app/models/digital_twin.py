"""
PHOENIX X — Phase X-093
Enterprise Cyber Digital Twin, Predictive Security Simulation & Attack Path Intelligence Platform
Database Models
"""
import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Boolean, DateTime, Float, ForeignKey, Integer,
    String, Text, JSON, Enum
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

# ─────────────────────────────────────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────────────────────────────────────

class AssetNodeType(str, enum.Enum):
    USER_IDENTITY = "USER_IDENTITY"
    MACHINE_IDENTITY = "MACHINE_IDENTITY"
    CLOUD_RESOURCE = "CLOUD_RESOURCE"
    NETWORK_NODE = "NETWORK_NODE"
    APPLICATION = "APPLICATION"

class SimulationStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class RiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"

# ─────────────────────────────────────────────────────────────────────────────
# Digital Twin Assets & Paths
# ─────────────────────────────────────────────────────────────────────────────

class TwinAssetNode(Base):
    """
    Represents an entity in the digital twin (asset, identity, cloud resource).
    """
    __tablename__ = "digital_twin_assets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    asset_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    node_type: Mapped[AssetNodeType] = mapped_column(Enum(AssetNodeType), nullable=False)
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    last_synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AttackPathGraph(Base):
    """
    Represents an identified attack path within the environment.
    """
    __tablename__ = "digital_twin_attack_paths"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    source_node_id: Mapped[str] = mapped_column(String(255), nullable=False) # Ext identifier or TwinAssetNode.id
    target_node_id: Mapped[str] = mapped_column(String(255), nullable=False)
    
    path_segments: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.MEDIUM)
    
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=True)
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Simulations & Analytics
# ─────────────────────────────────────────────────────────────────────────────

class SimulationScenario(Base):
    """
    Represents a "what-if" scenario and its predictive results.
    """
    __tablename__ = "digital_twin_simulations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hypothesis: Mapped[str] = mapped_column(Text, nullable=False)
    
    status: Mapped[SimulationStatus] = mapped_column(Enum(SimulationStatus), default=SimulationStatus.QUEUED)
    parameters: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    results: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class ResilienceMetric(Base):
    """
    Represents the assessed resilience score of an enterprise segment.
    """
    __tablename__ = "digital_twin_resilience"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    domain: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. "CLOUD", "IDENTITY", "ENTERPRISE"
    score: Mapped[float] = mapped_column(Float, default=0.0) # 0-100
    confidence_level: Mapped[float] = mapped_column(Float, default=0.0)
    
    contributing_factors: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OptimizationRecommendation(Base):
    """
    Simulation driven recommendation.
    """
    __tablename__ = "digital_twin_recommendations"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    result_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("digital_twin_simulations.id", ondelete="CASCADE"), index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    expected_impact: Mapped[str] = mapped_column(Text, nullable=False)
