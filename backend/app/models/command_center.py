import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class EnterpriseCloudMetric(Base):
    __tablename__ = "mf_cmd_enterprise_metrics"
    """
    High-level aggregated health scores across the entire cloud estate.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    metric_type: Mapped[str] = mapped_column(String(100)) # OVERALL_HEALTH, CSPM_SCORE, CWPP_SCORE, IDENTITY_HEALTH
    metric_value: Mapped[float] = mapped_column(Float)
    metric_trend: Mapped[str] = mapped_column(String(50)) # UP, DOWN, STABLE
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OperationalMetric(Base):
    __tablename__ = "mf_cmd_operational_metrics"
    """
    Metrics related to SOC and Cloud defense operations.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    metric_name: Mapped[str] = mapped_column(String(100)) # MTTD, MTTR, OPEN_CRITICAL_ALERTS
    metric_value: Mapped[float] = mapped_column(Float)
    
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CommandCenterAuditLog(Base):
    __tablename__ = "mf_cmd_audit_logs"
    """
    Immutable logs for human approval gates and executive decisions.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    action_type: Mapped[str] = mapped_column(String(100)) # APPROVE_REMEDIATION, OVERRIDE_RISK
    target_resource: Mapped[str] = mapped_column(String(255))
    actor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    justification: Mapped[str] = mapped_column(Text)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
