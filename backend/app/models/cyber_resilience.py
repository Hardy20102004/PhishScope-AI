"""
PHOENIX X — Phase X-095
Enterprise Cyber Resilience, Business Continuity & Continuous Readiness Platform
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

class CriticalityTier(str, enum.Enum):
    MISSION_CRITICAL = "MISSION_CRITICAL"
    BUSINESS_CRITICAL = "BUSINESS_CRITICAL"
    OPERATIONAL = "OPERATIONAL"
    SUPPORTING = "SUPPORTING"

class TestOutcome(str, enum.Enum):
    SUCCESS = "SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILURE = "FAILURE"
    UNTESTED = "UNTESTED"

class ExerciseStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# ─────────────────────────────────────────────────────────────────────────────
# Business Continuity & Objectives
# ─────────────────────────────────────────────────────────────────────────────

class BusinessServiceNode(Base):
    """
    Represents a critical business capability and its operational dependencies.
    """
    __tablename__ = "resilience_business_services"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    tier: Mapped[CriticalityTier] = mapped_column(Enum(CriticalityTier), default=CriticalityTier.OPERATIONAL)
    
    dependencies: Mapped[List[str]] = mapped_column(JSON, default=list) # App/Asset IDs
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RecoveryObjective(Base):
    """
    Tracks RTO (Recovery Time Objective) and RPO (Recovery Point Objective) metrics.
    """
    __tablename__ = "resilience_recovery_objectives"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resilience_business_services.id", ondelete="CASCADE"))
    
    rto_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    rpo_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    
    last_validated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

# ─────────────────────────────────────────────────────────────────────────────
# Disaster Recovery & Tabletops
# ─────────────────────────────────────────────────────────────────────────────

class DisasterRecoveryTest(Base):
    """
    Logs infrastructure and data backup tests and their outcomes.
    """
    __tablename__ = "resilience_dr_tests"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    test_name: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. "Cloud Prod", "Identity"
    
    outcome: Mapped[TestOutcome] = mapped_column(Enum(TestOutcome), default=TestOutcome.UNTESTED)
    actual_rto_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    findings: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    tested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class TabletopExercise(Base):
    """
    Manages crisis simulation exercises, scenarios, and findings.
    """
    __tablename__ = "resilience_tabletop_exercises"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_description: Mapped[str] = mapped_column(Text, nullable=False)
    
    status: Mapped[ExerciseStatus] = mapped_column(Enum(ExerciseStatus), default=ExerciseStatus.PLANNED)
    participants: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    lessons_learned: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    scheduled_for: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

# ─────────────────────────────────────────────────────────────────────────────
# Readiness Aggregation
# ─────────────────────────────────────────────────────────────────────────────

class ResilienceAssessment(Base):
    """
    Captures the overall continuous readiness assessment scores.
    """
    __tablename__ = "resilience_assessments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    overall_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    domain_scores: Mapped[Dict[str, float]] = mapped_column(JSON, default=dict) # e.g. {"BCP": 85, "DR": 92}
    
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
