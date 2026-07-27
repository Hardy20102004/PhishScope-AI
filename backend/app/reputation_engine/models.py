import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Text, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base

class ReputationTrend(str, enum.Enum):
    IMPROVING = "Improving"
    DECLINING = "Declining"
    STABLE = "Stable"
    VOLATILE = "Volatile"
    NEW = "New"

class ReputationProfile(Base):
    """
    Master record for an entity's current reputation.
    """
    __tablename__ = "reputation_profiles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True) # ID in Knowledge Graph or Indicator Table
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False) # 'Domain', 'IP', 'Threat Actor', etc.
    
    # Dual-metric approach
    risk_score: Mapped[float] = mapped_column(Float, default=0.0) # 0 to 100 (100 is highly malicious)
    trust_score: Mapped[float] = mapped_column(Float, default=50.0) # 0 to 100 (100 is highly trusted/allowlisted)
    
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    trend: Mapped[ReputationTrend] = mapped_column(Enum(ReputationTrend), default=ReputationTrend.NEW)
    
    first_observed: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True)

    history: Mapped[List["ReputationHistory"]] = relationship("ReputationHistory", back_populates="profile", cascade="all, delete-orphan")
    evidence: Mapped[List["ReputationEvidence"]] = relationship("ReputationEvidence", back_populates="profile", cascade="all, delete-orphan")

class ReputationHistory(Base):
    """
    Time-series ledger of score changes.
    """
    __tablename__ = "reputation_history"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("reputation_profiles.id", ondelete="CASCADE"), index=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    trust_score: Mapped[float] = mapped_column(Float, nullable=False)
    
    trigger_event: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # e.g., "New TI Feed Match", "Graph Influence"
    
    profile: Mapped["ReputationProfile"] = relationship("ReputationProfile", back_populates="history")

class ReputationEvidence(Base):
    """
    Underlying facts driving the reputation score.
    """
    __tablename__ = "reputation_evidence"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("reputation_profiles.id", ondelete="CASCADE"), index=True)
    
    source: Mapped[str] = mapped_column(String(255), nullable=False) # e.g., "CrowdStrike Feed", "Analyst Validation"
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Impact this evidence had
    risk_delta: Mapped[float] = mapped_column(Float, default=0.0) 
    trust_delta: Mapped[float] = mapped_column(Float, default=0.0)
    
    weight: Mapped[float] = mapped_column(Float, default=1.0) # Evidence weighting (decays over time)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    profile: Mapped["ReputationProfile"] = relationship("ReputationProfile", back_populates="evidence")
