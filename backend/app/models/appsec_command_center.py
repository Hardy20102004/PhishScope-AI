import uuid
from datetime import datetime, timezone
from typing import Optional
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class GovernanceDecisionStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class AppSecExecutiveMetric(Base):
    """
    Stores aggregated executive KPIs (e.g., Enterprise AppSec Risk Score, Compliance Posture) for board reporting.
    """
    __tablename__ = "appsec_executive_metrics"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    enterprise_risk_score: Mapped[float] = mapped_column(Float, default=0.0) # 0-100 scale
    compliance_posture: Mapped[float] = mapped_column(Float, default=0.0) # percentage compliant
    total_critical_vulnerabilities: Mapped[int] = mapped_column(Integer, default=0)
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EngineeringProductivityMetric(Base):
    """
    Correlates security operations with engineering velocity.
    """
    __tablename__ = "appsec_engineering_productivity"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    application_id: Mapped[str] = mapped_column(String(255), nullable=False)
    
    mean_time_to_remediate_days: Mapped[float] = mapped_column(Float, default=0.0)
    deployment_frequency_per_week: Mapped[float] = mapped_column(Float, default=0.0)
    security_friction_score: Mapped[float] = mapped_column(Float, default=0.0) # 0-100 (lower is better)
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AppSecConsolidatedFinding(Base):
    """
    A unified view of findings across SAST, DAST, SCA, Secrets, IaC for a given application.
    """
    __tablename__ = "appsec_consolidated_findings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    application_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_scanner: Mapped[str] = mapped_column(String(50), nullable=False) # e.g., SAST, DAST, SCA
    
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM")
    cwe_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    title: Mapped[str] = mapped_column(String(1024), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    is_remediated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AppSecGovernanceDecision(Base):
    """
    Logs executive or architect-level approvals for global AppSec policy adjustments.
    """
    __tablename__ = "appsec_governance_decisions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    policy_name: Mapped[str] = mapped_column(String(255), nullable=False)
    proposed_change: Mapped[str] = mapped_column(Text, nullable=False)
    
    status: Mapped[GovernanceDecisionStatus] = mapped_column(Enum(GovernanceDecisionStatus), default=GovernanceDecisionStatus.PENDING)
    
    requested_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
