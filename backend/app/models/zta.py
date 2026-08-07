"""
PHOENIX X — Phase X-082
Enterprise Zero Trust Architecture, Continuous Verification & Adaptive Access Platform
Database Models

Follows NIST SP 800-207 (Zero Trust Architecture) and NIST SP 800-63 (Digital Identity).
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

class VerificationType(str, enum.Enum):
    IDENTITY = "IDENTITY"
    DEVICE = "DEVICE"
    NETWORK = "NETWORK"
    SESSION = "SESSION"
    APPLICATION = "APPLICATION"


class AccessDecision(str, enum.Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    STEP_UP_AUTH = "STEP_UP_AUTH"
    REQUIRE_MFA = "REQUIRE_MFA"
    REQUIRE_COMPLIANT_DEVICE = "REQUIRE_COMPLIANT_DEVICE"
    ISOLATE_SESSION = "ISOLATE_SESSION"
    MONITOR = "MONITOR"


class SessionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    IDLE = "IDLE"
    TERMINATED_BY_USER = "TERMINATED_BY_USER"
    TERMINATED_BY_SYSTEM = "TERMINATED_BY_SYSTEM"
    REVOKED = "REVOKED"
    STEP_UP_PENDING = "STEP_UP_PENDING"


class PolicyEffect(str, enum.Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    CHALLENGE = "CHALLENGE"


class RiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NEGLIGIBLE = "NEGLIGIBLE"


class DeviceTrustStatus(str, enum.Enum):
    TRUSTED = "TRUSTED"
    MANAGED = "MANAGED"
    UNMANAGED = "UNMANAGED"
    COMPROMISED = "COMPROMISED"
    UNKNOWN = "UNKNOWN"


# ─────────────────────────────────────────────────────────────────────────────
# Zero Trust Context Snapshot
# ─────────────────────────────────────────────────────────────────────────────

class ZTAContextSnapshot(Base):
    """
    Point-in-time snapshot of context evaluated during an access request or continuous verification loop.
    Stores observed telemetry before any inferences are made.
    """
    __tablename__ = "zta_context_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    # Core Context Ties
    identity_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)
    device_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)
    application_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)

    # Observed Context Data (JSON)
    identity_context: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    device_context: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    network_context: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    location_context: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    auth_context: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Continuous Verification Record
# ─────────────────────────────────────────────────────────────────────────────

class ZTAVerificationRecord(Base):
    """
    Log of continuous verification checks executed in the background.
    """
    __tablename__ = "zta_verification_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    context_snapshot_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("zta_context_snapshots.id", ondelete="CASCADE"))

    verification_type: Mapped[VerificationType] = mapped_column(Enum(VerificationType), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    
    # Results
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True)
    findings: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)

    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Zero Trust Policy
# ─────────────────────────────────────────────────────────────────────────────

class ZTAPolicy(Base):
    """
    Adaptive access and Zero Trust policy definitions.
    Defines conditions under which access should be granted, denied, or challenged.
    """
    __tablename__ = "zta_policies"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    priority: Mapped[int] = mapped_column(Integer, default=100) # Lower number = higher priority

    # Policy Definition (JSON schema defining conditions: e.g. location, risk level, device status)
    conditions: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    # Outcomes
    effect: Mapped[PolicyEffect] = mapped_column(Enum(PolicyEffect), nullable=False)
    actions: Mapped[List[str]] = mapped_column(JSON, default=list) # Specific actions if CHALLENGE/DENY

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Adaptive Access Decision
# ─────────────────────────────────────────────────────────────────────────────

class ZTAAccessDecision(Base):
    """
    Records the outcome of evaluating a request against ZTA Policies.
    Provides explainability on exactly which policies triggered and why.
    """
    __tablename__ = "zta_access_decisions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    context_snapshot_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("zta_context_snapshots.id", ondelete="CASCADE"))
    
    decision: Mapped[AccessDecision] = mapped_column(Enum(AccessDecision), nullable=False, index=True)
    
    # Explainability
    matched_policy_ids: Mapped[List[str]] = mapped_column(JSON, default=list)
    rationale: Mapped[Text] = mapped_column(Text, nullable=True)
    
    # Metadata
    resource_requested: Mapped[str] = mapped_column(String(1024), nullable=False)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────────────────────

class ZTASessionState(Base):
    """
    Tracks active user/machine sessions, their current health, and risk levels.
    """
    __tablename__ = "zta_session_states"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    session_identifier: Mapped[str] = mapped_column(String(512), nullable=False, unique=True, index=True)
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    device_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    
    status: Mapped[SessionStatus] = mapped_column(Enum(SessionStatus), default=SessionStatus.ACTIVE, index=True)
    
    # Risk
    current_session_risk: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    anomalies_detected: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timing
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# Risk Evaluation
# ─────────────────────────────────────────────────────────────────────────────

class ZTARiskEvaluation(Base):
    """
    Point-in-time contextual risk calculation covering Identity, Device, Session, App.
    """
    __tablename__ = "zta_risk_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    context_snapshot_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("zta_context_snapshots.id", ondelete="CASCADE"))
    
    # Component Scores
    identity_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    device_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    session_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    app_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Aggregate
    composite_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW, index=True)
    
    # Explainability
    contributing_factors: Mapped[List[str]] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)

    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Policy Approval Workflow
# ─────────────────────────────────────────────────────────────────────────────

class ZTAPolicyApproval(Base):
    """
    Governance tracking for policy changes. Ensures all ZTA policy changes
    require explicit human approval.
    """
    __tablename__ = "zta_policy_approvals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    policy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("zta_policies.id", ondelete="CASCADE"))
    
    requested_by: Mapped[str] = mapped_column(String(512), nullable=False)
    requested_changes: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    justification: Mapped[Text] = mapped_column(Text, nullable=False)
    
    status: Mapped[str] = mapped_column(String(50), default="PENDING") # PENDING, APPROVED, REJECTED
    approved_by: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
