import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class StrategicForecast(Base):
    __tablename__ = "mf_sd_forecasts"
    """
    Predictive metrics on risk trends and control effectiveness over time.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    metric_name: Mapped[str] = mapped_column(String(100)) # e.g. MTT_CONTAIN, OVERALL_RESILIENCE
    target_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    projected_value: Mapped[float] = mapped_column(Float)
    confidence_score: Mapped[float] = mapped_column(Float) # 0.0 to 1.0
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class OptimizationRoadmap(Base):
    __tablename__ = "mf_sd_roadmaps"
    """
    A multi-phase security roadmap based on NIST CSF.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255))
    nist_function: Mapped[str] = mapped_column(String(50)) # IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER
    status: Mapped[str] = mapped_column(String(50)) # PLANNED, IN_PROGRESS, COMPLETED
    
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    target_end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class StrategicRecommendation(Base):
    __tablename__ = "mf_sd_recommendations"
    """
    Human-reviewable AI strategic recommendations.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    expected_impact: Mapped[str] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(50), default="PENDING_REVIEW") # PENDING_REVIEW, APPROVED, REJECTED
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DecisionApprovalLog(Base):
    __tablename__ = "mf_sd_approval_logs"
    """
    Immutable audit records tracking executive decisions on AI recommendations.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    recommendation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_sd_recommendations.id", ondelete="CASCADE"))
    executive_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    
    action_taken: Mapped[str] = mapped_column(String(50)) # APPROVED, REJECTED
    justification: Mapped[str] = mapped_column(Text, nullable=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
