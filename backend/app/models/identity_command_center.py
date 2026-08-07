"""
PHOENIX X — Phase X-090
Enterprise Unified Identity Security Command Center, Zero Trust Operations & Identity Intelligence Platform
Database Models
"""
import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from sqlalchemy import (
    Boolean, DateTime, Float, ForeignKey, Integer,
    String, Text, JSON, Enum
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

# ─────────────────────────────────────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────────────────────────────────────

class IdentityType(str, enum.Enum):
    HUMAN = "HUMAN"
    MACHINE = "MACHINE"
    WORKLOAD = "WORKLOAD"
    SERVICE_ACCOUNT = "SERVICE_ACCOUNT"

class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# ─────────────────────────────────────────────────────────────────────────────
# Portfolio & Health
# ─────────────────────────────────────────────────────────────────────────────

class EnterpriseIdentityPortfolio(Base):
    """
    High-level aggregation of all identities (human and machine) across the enterprise.
    """
    __tablename__ = "identity_cc_portfolio"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True, unique=True)
    identity_type: Mapped[IdentityType] = mapped_column(Enum(IdentityType), nullable=False)
    
    is_privileged: Mapped[bool] = mapped_column(Boolean, default=False)
    is_federated: Mapped[bool] = mapped_column(Boolean, default=False)
    
    managed_by: Mapped[str] = mapped_column(String(255), nullable=True) # e.g. "Okta", "AWS IAM"
    
    last_correlated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class IdentityHealthMetric(Base):
    """
    Unified health scores for authentication, privilege, lifecycle, and federation.
    """
    __tablename__ = "identity_cc_health_metrics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    auth_health: Mapped[float] = mapped_column(Float, default=100.0)
    privilege_health: Mapped[float] = mapped_column(Float, default=100.0)
    lifecycle_health: Mapped[float] = mapped_column(Float, default=100.0)
    federation_health: Mapped[float] = mapped_column(Float, default=100.0)
    zero_trust_health: Mapped[float] = mapped_column(Float, default=100.0)
    
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Executive Governance & Logging
# ─────────────────────────────────────────────────────────────────────────────

class ExecutiveDecisionLog(Base):
    """
    Audit trail of human-approved strategic identity policies and governance decisions.
    """
    __tablename__ = "identity_cc_decision_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    decision_type: Mapped[str] = mapped_column(String(255), nullable=False) # e.g., "REVOKE_FEDERATION_TRUST"
    justification: Mapped[str] = mapped_column(Text, nullable=False)
    
    approver_id: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    
    metadata_context: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
