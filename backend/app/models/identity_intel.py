"""
PHOENIX X — Phase X-089
Enterprise Identity Risk Analytics, Behavioral Identity Intelligence & Adaptive Trust Scoring Platform
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

class TelemetrySource(str, enum.Enum):
    PAM = "PAM"
    IGA = "IGA"
    AUTHN = "AUTHN"
    ITDR = "ITDR"
    FEDERATION = "FEDERATION"
    CLOUD_IAM = "CLOUD_IAM"

class TrustLevel(str, enum.Enum):
    HIGH_TRUST = "HIGH_TRUST"
    MEDIUM_TRUST = "MEDIUM_TRUST"
    LOW_TRUST = "LOW_TRUST"
    ZERO_TRUST = "ZERO_TRUST"

class RiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class BehaviorDeviation(str, enum.Enum):
    NORMAL = "NORMAL"
    SLIGHT_DEVIATION = "SLIGHT_DEVIATION"
    ANOMALOUS = "ANOMALOUS"


# ─────────────────────────────────────────────────────────────────────────────
# Telemetry & Behavior
# ─────────────────────────────────────────────────────────────────────────────

class IdentityTelemetry(Base):
    """
    Aggregated identity events from authentication, PAM, IGA, and Federation sources.
    """
    __tablename__ = "identity_intel_telemetry"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    source: Mapped[TelemetrySource] = mapped_column(Enum(TelemetrySource), nullable=False)
    
    event_type: Mapped[str] = mapped_column(String(255), nullable=False)
    context_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class BehaviorBaseline(Base):
    """
    Derived behavioral profiles for users based on time, location, and application access patterns.
    """
    __tablename__ = "identity_intel_behavior_baselines"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True, unique=True)
    
    typical_devices: Mapped[List[str]] = mapped_column(JSON, default=list)
    typical_locations: Mapped[List[str]] = mapped_column(JSON, default=list)
    typical_active_hours: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    current_deviation: Mapped[BehaviorDeviation] = mapped_column(Enum(BehaviorDeviation), default=BehaviorDeviation.NORMAL)
    
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Trust Scoring
# ─────────────────────────────────────────────────────────────────────────────

class AdaptiveTrustScore(Base):
    """
    Dynamic identity trust scores, combining hygiene, behavior, and authentication confidence.
    """
    __tablename__ = "identity_intel_trust_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True, unique=True)
    
    composite_score: Mapped[float] = mapped_column(Float, default=100.0) # 0 to 100
    behavior_confidence: Mapped[float] = mapped_column(Float, default=100.0)
    auth_assurance_confidence: Mapped[float] = mapped_column(Float, default=100.0)
    hygiene_confidence: Mapped[float] = mapped_column(Float, default=100.0)
    
    trust_level: Mapped[TrustLevel] = mapped_column(Enum(TrustLevel), default=TrustLevel.HIGH_TRUST)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Risk Analytics
# ─────────────────────────────────────────────────────────────────────────────

class IdentityRiskAnalytics(Base):
    """
    Continuous identity risk analytics and executive metrics.
    """
    __tablename__ = "identity_intel_risk_analytics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True, unique=True)
    
    overall_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    privilege_risk: Mapped[float] = mapped_column(Float, default=0.0)
    operational_risk: Mapped[float] = mapped_column(Float, default=0.0)
    
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
