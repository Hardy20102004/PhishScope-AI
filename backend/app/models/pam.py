"""
PHOENIX X — Phase X-083
Enterprise Privileged Access Management (PAM), Just-in-Time (JIT) Access & Administrative Session Governance Platform
Database Models

Follows NIST SP 800-63, NIST SP 800-207 (Zero Trust Architecture).
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

class PrivilegedIdentityType(str, enum.Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    SERVICE_ACCOUNT = "SERVICE_ACCOUNT"
    BREAK_GLASS = "BREAK_GLASS"
    MACHINE_IDENTITY = "MACHINE_IDENTITY"
    DELEGATED_ADMIN = "DELEGATED_ADMIN"

class JITRequestStatus(str, enum.Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    PROVISIONING_FAILED = "PROVISIONING_FAILED"

class AdminSessionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    TERMINATED_BY_POLICY = "TERMINATED_BY_POLICY"
    TERMINATED_BY_ADMIN = "TERMINATED_BY_ADMIN"
    ANOMALOUS = "ANOMALOUS"

class CredentialStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    ROTATION_PENDING = "ROTATION_PENDING"
    COMPROMISED = "COMPROMISED"
    REVOKED = "REVOKED"

class PrivilegeRiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NEGLIGIBLE = "NEGLIGIBLE"


# ─────────────────────────────────────────────────────────────────────────────
# Privileged Identity Inventory
# ─────────────────────────────────────────────────────────────────────────────

class PAMPrivilegedIdentity(Base):
    """
    Inventory of standing privileges, administrative accounts, break-glass accounts,
    and service accounts requiring special governance.
    """
    __tablename__ = "pam_privileged_identities"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    # Links to the unified ISPM identity if applicable
    ispm_identity_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)

    identity_type: Mapped[PrivilegedIdentityType] = mapped_column(Enum(PrivilegedIdentityType), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(512), nullable=False)
    principal_name: Mapped[str] = mapped_column(String(512), nullable=False)
    
    # Discovery context
    source_platform: Mapped[str] = mapped_column(String(255), nullable=False)  # e.g., Entra ID, AWS IAM, GCP
    is_standing_privilege: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Ownership
    owner_email: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    business_justification: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Risk metrics
    privilege_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_level: Mapped[PrivilegeRiskLevel] = mapped_column(Enum(PrivilegeRiskLevel), default=PrivilegeRiskLevel.LOW)

    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# JIT Access Workflow
# ─────────────────────────────────────────────────────────────────────────────

class PAMJITRequest(Base):
    """
    Workflow state for Just-In-Time access elevation requests.
    """
    __tablename__ = "pam_jit_requests"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    requester_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    target_role: Mapped[str] = mapped_column(String(512), nullable=False)
    target_resource: Mapped[str] = mapped_column(String(512), nullable=False)
    
    justification: Mapped[Text] = mapped_column(Text, nullable=False)
    ticket_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # e.g. Jira/ServiceNow issue
    
    requested_duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    
    status: Mapped[JITRequestStatus] = mapped_column(Enum(JITRequestStatus), default=JITRequestStatus.PENDING_APPROVAL, index=True)
    
    # Approvals
    approved_by: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    approval_notes: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    
    # Timing
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    activated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# Administrative Session Metadata
# ─────────────────────────────────────────────────────────────────────────────

class PAMSessionRecord(Base):
    """
    Metadata for governed administrative sessions.
    (Note: Never stores sensitive keystrokes or raw video here).
    """
    __tablename__ = "pam_session_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    # Link to JIT if applicable, otherwise a standing access session
    jit_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("pam_jit_requests.id", ondelete="SET NULL"), nullable=True)
    
    identity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    target_resource: Mapped[str] = mapped_column(String(512), nullable=False)
    
    status: Mapped[AdminSessionStatus] = mapped_column(Enum(AdminSessionStatus), default=AdminSessionStatus.ACTIVE, index=True)
    
    # Telemetry
    ip_address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mfa_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    session_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Audit Trail Link
    recording_vault_reference: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# Credential Lifecycle Governance
# ─────────────────────────────────────────────────────────────────────────────

class PAMCredentialLifecycle(Base):
    """
    Oversight records for vault credentials and their rotation status.
    """
    __tablename__ = "pam_credential_lifecycles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("pam_privileged_identities.id", ondelete="SET NULL"), nullable=True)
    
    credential_name: Mapped[str] = mapped_column(String(512), nullable=False)
    credential_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. PASSWORD, API_KEY, CERTIFICATE, SSH_KEY
    
    vault_reference: Mapped[str] = mapped_column(String(1024), nullable=False)
    
    status: Mapped[CredentialStatus] = mapped_column(Enum(CredentialStatus), default=CredentialStatus.ACTIVE, index=True)
    
    # Rotation Policy
    rotation_interval_days: Mapped[int] = mapped_column(Integer, default=30)
    last_rotated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    policy_compliant: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# PAM Policies
# ─────────────────────────────────────────────────────────────────────────────

class PAMPolicy(Base):
    """
    Privilege governance policies (e.g. required approvals for AWS Prod, max duration for JIT).
    """
    __tablename__ = "pam_policies"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # JSON schema detailing target scopes, required approvals, max durations
    rules: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Risk Scores (Privilege Specific)
# ─────────────────────────────────────────────────────────────────────────────

class PAMRiskScore(Base):
    """
    Specialized risk scoring for privileged accounts and sessions.
    """
    __tablename__ = "pam_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False) # IDENTITY, SESSION, CREDENTIAL
    entity_id: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_level: Mapped[PrivilegeRiskLevel] = mapped_column(Enum(PrivilegeRiskLevel), default=PrivilegeRiskLevel.LOW, index=True)
    
    contributing_factors: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
