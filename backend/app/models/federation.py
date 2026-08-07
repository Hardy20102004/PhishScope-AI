"""
PHOENIX X — Phase X-088
Enterprise Federated Identity, Single Sign-On (SSO) & Cross-Domain Trust Intelligence Platform
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

class FederationRole(str, enum.Enum):
    IDENTITY_PROVIDER = "IDENTITY_PROVIDER"
    SERVICE_PROVIDER = "SERVICE_PROVIDER"
    IDENTITY_BROKER = "IDENTITY_BROKER"

class ProtocolType(str, enum.Enum):
    SAML_2_0 = "SAML_2_0"
    OIDC = "OIDC"
    OAUTH_2_0 = "OAUTH_2_0"
    WS_FEDERATION = "WS_FEDERATION"
    SCIM = "SCIM"

class TrustStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING_METADATA = "PENDING_METADATA"
    DEPRECATED = "DEPRECATED"

class RiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ─────────────────────────────────────────────────────────────────────────────
# Federation Inventory
# ─────────────────────────────────────────────────────────────────────────────

class FederatedProvider(Base):
    """
    Inventory of Identity Providers (IdP), Service Providers (SP), and Brokers.
    """
    __tablename__ = "federation_providers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    role: Mapped[FederationRole] = mapped_column(Enum(FederationRole), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(1024), nullable=False) # SAML EntityID / OIDC Issuer
    
    business_owner: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    environment: Mapped[str] = mapped_column(String(255), default="Production")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class FederationTrust(Base):
    """
    Tracks trust relationships and mappings between IdPs and SPs.
    """
    __tablename__ = "federation_trusts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    idp_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("federation_providers.id", ondelete="CASCADE"))
    sp_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("federation_providers.id", ondelete="CASCADE"))
    
    protocol: Mapped[ProtocolType] = mapped_column(Enum(ProtocolType), nullable=False)
    status: Mapped[TrustStatus] = mapped_column(Enum(TrustStatus), default=TrustStatus.ACTIVE)
    
    attribute_mapping: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict) # e.g. mapping internal claims to SAML assertions
    
    established_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ─────────────────────────────────────────────────────────────────────────────
# Metadata & Certificates
# ─────────────────────────────────────────────────────────────────────────────

class FederationCertificate(Base):
    """
    Tracks signing certificates used in SAML/OIDC flows and their lifecycle.
    """
    __tablename__ = "federation_certificates"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    provider_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("federation_providers.id", ondelete="CASCADE"))
    
    common_name: Mapped[str] = mapped_column(String(512), nullable=False)
    thumbprint: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    valid_to: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class FederationProtocolConfig(Base):
    """
    Configuration metadata for SAML, OIDC, OAuth, etc.
    """
    __tablename__ = "federation_protocol_configs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    trust_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("federation_trusts.id", ondelete="CASCADE"), unique=True)
    
    requires_signed_assertions: Mapped[bool] = mapped_column(Boolean, default=True)
    requires_encrypted_assertions: Mapped[bool] = mapped_column(Boolean, default=False)
    allowed_redirect_uris: Mapped[List[str]] = mapped_column(JSON, default=list) # For OIDC/OAuth
    
    metadata_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# Risk Score
# ─────────────────────────────────────────────────────────────────────────────

class FederationRiskScore(Base):
    """
    Risk score evaluating weak protocols, expiring metadata certs, and over-permissive trusts.
    """
    __tablename__ = "federation_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    trust_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("federation_trusts.id", ondelete="CASCADE"), index=True)
    
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    protocol_risk: Mapped[float] = mapped_column(Float, default=0.0)
    certificate_risk: Mapped[float] = mapped_column(Float, default=0.0)
    
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
