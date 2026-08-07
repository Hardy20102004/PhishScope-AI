import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class AITriageGroup(Base):
    __tablename__ = "ai_triage_groups"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255))
    grouping_reason: Mapped[str] = mapped_column(String(255)) # E.g., SHARED_IOC, ALERT_STORM, MULTIPLE_ALERTS_ON_HOST
    confidence: Mapped[float] = mapped_column(Float, default=0.0) # Grouping confidence
    
    # Priority & Impact
    overall_priority_score: Mapped[float] = mapped_column(Float, default=0.0)
    business_impact_score: Mapped[float] = mapped_column(Float, default=0.0)
    priority_tier: Mapped[str] = mapped_column(String(50), default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    
    status: Mapped[str] = mapped_column(String(50), default="OPEN", index=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    recommendation = relationship("AlertRecommendation", back_populates="triage_group", uselist=False, cascade="all, delete-orphan")
    feedback = relationship("AnalystFeedback", back_populates="triage_group", cascade="all, delete-orphan")
    
    # Alerts in this group would ideally be linked via an association table or adding ai_triage_group_id to Alert model.
    # Since Alert model is in alert_management.py, we'd add it there or just use this group ID.


class AlertRecommendation(Base):
    __tablename__ = "ai_alert_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    triage_group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_triage_groups.id", ondelete="CASCADE"), unique=True, index=True)
    
    alert_summary: Mapped[str] = mapped_column(Text)
    priority_explanation: Mapped[str] = mapped_column(Text)
    business_impact_summary: Mapped[str] = mapped_column(Text)
    
    investigation_steps: Mapped[List[str]] = mapped_column(JSON, default=list)
    alternative_interpretations: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    ai_confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    uncertainty_factors: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    triage_group = relationship("AITriageGroup", back_populates="recommendation")


class AnalystFeedback(Base):
    __tablename__ = "ai_analyst_feedback"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    triage_group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_triage_groups.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    feedback_type: Mapped[str] = mapped_column(String(50)) # FALSE_POSITIVE, TRUE_POSITIVE, PRIORITY_OVERRIDE, BAD_RECOMMENDATION
    priority_override: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # If they changed it
    
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    processed_by_learning_engine: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    triage_group = relationship("AITriageGroup", back_populates="feedback")


class AssetBusinessContext(Base):
    __tablename__ = "asset_business_context"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    asset_identifier: Mapped[str] = mapped_column(String(255), index=True) # IP, Hostname
    criticality_score: Mapped[float] = mapped_column(Float, default=5.0) # 1-10
    business_service: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    data_sensitivity: Mapped[str] = mapped_column(String(50), default="NORMAL") # LOW, NORMAL, RESTRICTED, CONFIDENTIAL
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
