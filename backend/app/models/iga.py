"""
PHOENIX X — Phase X-085
Enterprise Identity Governance & Administration (IGA) Platform
Database Models

Follows NIST SP 800-63, NIST SP 800-207.
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

class JMLEventType(str, enum.Enum):
    JOINER = "JOINER"
    MOVER = "MOVER"
    LEAVER = "LEAVER"
    CONTRACTOR_EXTENSION = "CONTRACTOR_EXTENSION"

class JMLStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    MANUAL_INTERVENTION_REQUIRED = "MANUAL_INTERVENTION_REQUIRED"

class AccessRequestStatus(str, enum.Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PROVISIONING = "PROVISIONING"
    PROVISIONED = "PROVISIONED"
    PROVISIONING_FAILED = "PROVISIONING_FAILED"

class CertificationStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"

class CertificationDecision(str, enum.Enum):
    APPROVE = "APPROVE"
    REVOKE = "REVOKE"
    DELEGATE = "DELEGATE"
    ACKNOWLEDGE = "ACKNOWLEDGE" # for informational items

class SoDSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class RiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ─────────────────────────────────────────────────────────────────────────────
# Joiner-Mover-Leaver (JML)
# ─────────────────────────────────────────────────────────────────────────────

class IGALifecycleEvent(Base):
    """
    Records of JML events.
    """
    __tablename__ = "iga_lifecycle_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    event_type: Mapped[JMLEventType] = mapped_column(Enum(JMLEventType), nullable=False, index=True)
    status: Mapped[JMLStatus] = mapped_column(Enum(JMLStatus), default=JMLStatus.PENDING)
    
    source_system: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. Workday, SAP
    effective_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict) # e.g. new department, title
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Access Requests
# ─────────────────────────────────────────────────────────────────────────────

class IGAAccessRequest(Base):
    """
    User requests for entitlements/roles.
    """
    __tablename__ = "iga_access_requests"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    requester_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    target_identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True) # Usually same as requester, but can be for someone else
    
    entitlement_id: Mapped[str] = mapped_column(String(512), nullable=False)
    justification: Mapped[Text] = mapped_column(Text, nullable=False)
    
    status: Mapped[AccessRequestStatus] = mapped_column(Enum(AccessRequestStatus), default=AccessRequestStatus.PENDING_APPROVAL)
    
    approver_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    approval_notes: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True) # For temporary access
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Access Certifications (UAR)
# ─────────────────────────────────────────────────────────────────────────────

class IGACertificationCampaign(Base):
    """
    Periodic access reviews (UAR).
    """
    __tablename__ = "iga_certification_campaigns"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=True)
    
    status: Mapped[CertificationStatus] = mapped_column(Enum(CertificationStatus), default=CertificationStatus.DRAFT)
    
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    total_items: Mapped[int] = mapped_column(Integer, default=0)
    completed_items: Mapped[int] = mapped_column(Integer, default=0)


class IGACertificationItem(Base):
    """
    Individual entitlement reviews within a campaign.
    """
    __tablename__ = "iga_certification_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    campaign_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("iga_certification_campaigns.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False)
    entitlement_id: Mapped[str] = mapped_column(String(512), nullable=False)
    
    reviewer_id: Mapped[str] = mapped_column(String(512), nullable=False)
    
    decision: Mapped[Optional[CertificationDecision]] = mapped_column(Enum(CertificationDecision), nullable=True)
    decision_notes: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    decision_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# Segregation of Duties (SoD)
# ─────────────────────────────────────────────────────────────────────────────

class IGASegregationOfDutiesRule(Base):
    """
    Defined SoD rules (e.g., Cannot be both AP Clerk and AP Manager).
    """
    __tablename__ = "iga_sod_rules"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    
    conflicting_entitlements: Mapped[List[str]] = mapped_column(JSON, default=list) # List of entitlement IDs
    severity: Mapped[SoDSeverity] = mapped_column(Enum(SoDSeverity), default=SoDSeverity.HIGH)
    
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class IGASoDViolation(Base):
    """
    Detected violations of SoD rules.
    """
    __tablename__ = "iga_sod_violations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    rule_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("iga_sod_rules.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolution_notes: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# IGA Risk
# ─────────────────────────────────────────────────────────────────────────────

class IGARiskScore(Base):
    """
    Identity Governance Risk score.
    """
    __tablename__ = "iga_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    access_risk: Mapped[float] = mapped_column(Float, default=0.0)
    sod_risk: Mapped[float] = mapped_column(Float, default=0.0)
    
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
