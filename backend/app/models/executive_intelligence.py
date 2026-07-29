import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class GovernanceMetric(Base):
    __tablename__ = "mf_ei_governance_metrics"
    """
    Tracks compliance, policy adherence, and roadmap progress.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    framework: Mapped[str] = mapped_column(String(100)) # e.g. NIST CSF, ISO 27001
    metric_name: Mapped[str] = mapped_column(String(255))
    compliance_score: Mapped[float] = mapped_column(Float) # 0 to 100
    
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class BusinessImpactIndicator(Base):
    __tablename__ = "mf_ei_business_impact"
    """
    Translates technical risk into business service impact.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    service_name: Mapped[str] = mapped_column(String(255))
    criticality: Mapped[str] = mapped_column(String(50)) # MISSION_CRITICAL, HIGH, MEDIUM, LOW
    
    current_risk_score: Mapped[float] = mapped_column(Float) # 0-100 scale, higher is riskier
    availability_status: Mapped[str] = mapped_column(String(50)) # ONLINE, DEGRADED, AT_RISK
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class InvestmentROI(Base):
    __tablename__ = "mf_ei_investment_roi"
    """
    Tracks operational efficiency gains per strategic initiative.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    initiative_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50)) # PLANNED, ACTIVE, COMPLETED
    
    hours_saved_monthly: Mapped[float] = mapped_column(Float, default=0.0)
    risk_reduction_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DecisionSupportBrief(Base):
    __tablename__ = "mf_ei_decision_briefs"
    """
    Pre-computed strategic briefs generated for executive review.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255))
    executive_summary: Mapped[str] = mapped_column(Text)
    recommendations: Mapped[dict] = mapped_column(JSON, default=list) # List of strings
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
