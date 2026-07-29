import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class CyberResilienceScore(Base):
    __tablename__ = "mf_cr_scores"
    """
    The top-level executive score representing overall cyber resilience.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Core pillars
    preventive_effectiveness: Mapped[float] = mapped_column(Float, default=0.0)
    detective_effectiveness: Mapped[float] = mapped_column(Float, default=0.0)
    response_effectiveness: Mapped[float] = mapped_column(Float, default=0.0)
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class MaturityAssessment(Base):
    __tablename__ = "mf_cr_maturity"
    """
    Domain-specific maturity scores (Tier 1-5).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    domain: Mapped[str] = mapped_column(String(100)) # e.g. SOC, INCIDENT_RESPONSE, DETECTION_ENGINEERING
    maturity_tier: Mapped[int] = mapped_column(Integer) # 1 = Initial, 2 = Managed, 3 = Defined, 4 = Quantitatively Managed, 5 = Optimizing
    
    justification: Mapped[str] = mapped_column(Text)
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ExecutiveKPI(Base):
    __tablename__ = "mf_cr_kpis"
    """
    Individual board-level metrics.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    metric_name: Mapped[str] = mapped_column(String(100)) # e.g. MTT_CONTAIN, BAS_SUCCESS_RATE
    metric_value: Mapped[float] = mapped_column(Float)
    metric_unit: Mapped[str] = mapped_column(String(50)) # e.g. HOURS, PERCENTAGE
    
    trend: Mapped[str] = mapped_column(String(50)) # IMPROVING, DEGRADING, STABLE
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
