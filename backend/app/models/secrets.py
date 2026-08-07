import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class SecretType(str, enum.Enum):
    API_KEY = "API_KEY"
    ACCESS_TOKEN = "ACCESS_TOKEN"
    OAUTH_TOKEN = "OAUTH_TOKEN"
    JWT_METADATA = "JWT_METADATA"
    SSH_KEY = "SSH_KEY"
    TLS_CERTIFICATE = "TLS_CERTIFICATE"
    PRIVATE_KEY = "PRIVATE_KEY"
    CLOUD_ACCESS_KEY = "CLOUD_ACCESS_KEY"
    DATABASE_CREDENTIAL = "DATABASE_CREDENTIAL"
    UNKNOWN = "UNKNOWN"

class SecretLifecycleStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ROTATING = "ROTATING"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"

class SecretMetadata(Base):
    """
    Represents a discovered credential (metadata only).
    """
    __tablename__ = "secrets_metadata"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    secret_type: Mapped[SecretType] = mapped_column(Enum(SecretType), default=SecretType.UNKNOWN)
    name: Mapped[str] = mapped_column(String(255), nullable=False) # E.g., "AWS Prod Access Key"
    
    # Hash or prefix used for correlation, NOT the secret itself
    identifier_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) 
    
    location_uri: Mapped[str] = mapped_column(String(1024), nullable=False) # e.g., github repo url, vault path
    
    lifecycle_status: Mapped[SecretLifecycleStatus] = mapped_column(Enum(SecretLifecycleStatus), default=SecretLifecycleStatus.ACTIVE)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_rotated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

class SecretExposure(Base):
    """
    Captures risk events associated with a secret.
    """
    __tablename__ = "secrets_exposure"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    secret_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("secrets_metadata.id", ondelete="CASCADE"), index=True)
    
    exposure_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g., HARDCODED, DORMANT, EXPIRED
    severity: Mapped[str] = mapped_column(String(50), default="HIGH")
    
    details: Mapped[str] = mapped_column(Text, nullable=False)
    
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecretPolicy(Base):
    """
    Defines enterprise standards for secrets.
    """
    __tablename__ = "secrets_policies"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    target_secret_type: Mapped[SecretType] = mapped_column(Enum(SecretType), default=SecretType.UNKNOWN)
    max_age_days: Mapped[int] = mapped_column(Integer, default=90)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class SecretGuidance(Base):
    """
    Captures AI-generated remediation advice.
    """
    __tablename__ = "secrets_guidance"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    exposure_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("secrets_exposure.id", ondelete="CASCADE"), unique=True)
    
    remediation_steps: Mapped[str] = mapped_column(Text, nullable=False)
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecretsAuditLog(Base):
    """
    Audit log for secrets governance.
    """
    __tablename__ = "secrets_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
