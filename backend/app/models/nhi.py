"""
PHOENIX X — Phase X-086
Enterprise Machine Identity, Workload Identity & Non-Human Identity Security Platform
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

class MachineIdentityType(str, enum.Enum):
    SERVICE_ACCOUNT = "SERVICE_ACCOUNT"
    API_KEY = "API_KEY"
    WORKLOAD_IDENTITY = "WORKLOAD_IDENTITY"
    K8S_SERVICE_ACCOUNT = "K8S_SERVICE_ACCOUNT"
    SERVERLESS_FUNCTION = "SERVERLESS_FUNCTION"
    AI_AGENT = "AI_AGENT"
    IOT_DEVICE = "IOT_DEVICE"

class CredentialStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    ROTATION_REQUIRED = "ROTATION_REQUIRED"
    COMPROMISED = "COMPROMISED"

class TrustType(str, enum.Enum):
    CROSS_ACCOUNT = "CROSS_ACCOUNT"
    FEDERATED = "FEDERATED"
    OIDC = "OIDC"
    SPIFFE = "SPIFFE"
    APP_TO_APP = "APP_TO_APP"

class RiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ─────────────────────────────────────────────────────────────────────────────
# Core Inventory
# ─────────────────────────────────────────────────────────────────────────────

class NHIMachineIdentity(Base):
    """
    Central inventory for Service Accounts, API Keys, Workload Identities, etc.
    """
    __tablename__ = "nhi_identities"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    identity_type: Mapped[MachineIdentityType] = mapped_column(Enum(MachineIdentityType), nullable=False, index=True)
    
    provider: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. AWS, GCP, Entra, K8s
    environment: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. Production, Dev
    
    owner_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True) # Human owner
    
    credential_status: Mapped[CredentialStatus] = mapped_column(Enum(CredentialStatus), default=CredentialStatus.ACTIVE)
    last_rotated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class NHICertificate(Base):
    """
    Inventory of certificates and their trust chains.
    """
    __tablename__ = "nhi_certificates"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    common_name: Mapped[str] = mapped_column(String(512), nullable=False)
    serial_number: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    issuer: Mapped[str] = mapped_column(String(512), nullable=False)
    
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    valid_to: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    identity_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("nhi_identities.id", ondelete="SET NULL"), nullable=True)
    
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)


# ─────────────────────────────────────────────────────────────────────────────
# Trust & Relationships
# ─────────────────────────────────────────────────────────────────────────────

class NHITrustRelationship(Base):
    """
    Mappings of trust between identities, services, and workloads.
    """
    __tablename__ = "nhi_trust_relationships"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    source_identity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nhi_identities.id", ondelete="CASCADE"), index=True)
    target_resource_arn: Mapped[str] = mapped_column(String(1024), nullable=False) # The resource/service being accessed
    
    trust_type: Mapped[TrustType] = mapped_column(Enum(TrustType), nullable=False)
    
    permissions: Mapped[List[str]] = mapped_column(JSON, default=list) # e.g. ["s3:GetObject", "sts:AssumeRole"]
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Lifecycle & Risk
# ─────────────────────────────────────────────────────────────────────────────

class NHILifecycleEvent(Base):
    """
    Records of non-human identity creation, rotation, and revocation.
    """
    __tablename__ = "nhi_lifecycle_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    identity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nhi_identities.id", ondelete="CASCADE"), index=True)
    
    event_type: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. CREATED, ROTATED, REVOKED
    actor_id: Mapped[str] = mapped_column(String(512), nullable=False) # Who/what triggered it
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class NHIRiskScore(Base):
    """
    Machine Identity Governance Risk score.
    """
    __tablename__ = "nhi_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nhi_identities.id", ondelete="CASCADE"), index=True)
    
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    over_permission_risk: Mapped[float] = mapped_column(Float, default=0.0)
    stale_credential_risk: Mapped[float] = mapped_column(Float, default=0.0)
    
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
