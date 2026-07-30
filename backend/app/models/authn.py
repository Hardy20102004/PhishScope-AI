"""
PHOENIX X — Phase X-087
Enterprise Passwordless Authentication, Passkey Governance & Modern Authentication Intelligence Platform
Database Models
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

class AuthnMethodType(str, enum.Enum):
    PASSKEY = "PASSKEY"
    FIDO2_HARDWARE = "FIDO2_HARDWARE"
    BIOMETRIC_LOCAL = "BIOMETRIC_LOCAL"
    TOTP = "TOTP"
    PUSH_NOTIFICATION = "PUSH_NOTIFICATION"
    SMS_OTP = "SMS_OTP"
    EMAIL_OTP = "EMAIL_OTP"
    PASSWORD = "PASSWORD"
    CERTIFICATE = "CERTIFICATE"

class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PENDING_ACTIVATION = "PENDING_ACTIVATION"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"

class AssuranceLevel(str, enum.Enum):
    AAL1 = "AAL1" # Single factor
    AAL2 = "AAL2" # Two factor, phishable
    AAL3 = "AAL3" # Hardware-backed, phishing-resistant

class RiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ─────────────────────────────────────────────────────────────────────────────
# Authentication Inventory
# ─────────────────────────────────────────────────────────────────────────────

class AuthnMethod(Base):
    """
    Central inventory of available authentication methods across the enterprise.
    """
    __tablename__ = "authn_methods"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    type: Mapped[AuthnMethodType] = mapped_column(Enum(AuthnMethodType), nullable=False)
    
    provider: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. Entra, Okta, Duo
    is_phishing_resistant: Mapped[bool] = mapped_column(Boolean, default=False)
    
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AuthnEnrollment(Base):
    """
    Tracks identity enrollments into specific authenticators.
    """
    __tablename__ = "authn_enrollments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    method_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("authn_methods.id", ondelete="CASCADE"), index=True)
    
    device_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True) # Device bound passkeys/hardware tokens
    
    status: Mapped[EnrollmentStatus] = mapped_column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Policies & Assurance
# ─────────────────────────────────────────────────────────────────────────────

class AuthnPolicy(Base):
    """
    Governing policies mapping required authentication strengths to resources.
    """
    __tablename__ = "authn_policies"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=True)
    
    target_group: Mapped[str] = mapped_column(String(512), nullable=False) # e.g. "Admins", "All Users"
    required_aal: Mapped[AssuranceLevel] = mapped_column(Enum(AssuranceLevel), default=AssuranceLevel.AAL2)
    
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class AuthnAssuranceLevel(Base):
    """
    Tracks the calculated Authentication Assurance Level (AAL) for identities.
    """
    __tablename__ = "authn_assurance_levels"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    
    current_aal: Mapped[AssuranceLevel] = mapped_column(Enum(AssuranceLevel), default=AssuranceLevel.AAL1)
    highest_capable_aal: Mapped[AssuranceLevel] = mapped_column(Enum(AssuranceLevel), default=AssuranceLevel.AAL1)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Risk Score
# ─────────────────────────────────────────────────────────────────────────────

class AuthnRiskScore(Base):
    """
    Risk score evaluating weak authentication, poor coverage, and unrotated recovery methods.
    """
    __tablename__ = "authn_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    weak_mfa_risk: Mapped[float] = mapped_column(Float, default=0.0)
    recovery_risk: Mapped[float] = mapped_column(Float, default=0.0)
    
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
