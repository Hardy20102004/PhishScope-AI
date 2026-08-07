import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class CIEMCloudIdentity(Base):
    __tablename__ = "mf_ciem_identities"
    """
    Inventory of discovered Users, Groups, and Roles across providers.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_name: Mapped[str] = mapped_column(String(255))
    identity_type: Mapped[str] = mapped_column(String(50)) # USER, GROUP, ROLE, SERVICE_ACCOUNT
    provider: Mapped[str] = mapped_column(String(50)) # AWS, AZURE, GCP, OKTA
    account_id: Mapped[str] = mapped_column(String(100))
    
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CloudEntitlement(Base):
    __tablename__ = "mf_ciem_entitlements"
    """
    Calculated effective permissions an identity holds.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_ciem_identities.id", ondelete="CASCADE"), index=True)
    
    resource_type: Mapped[str] = mapped_column(String(100)) # e.g. "s3:bucket", "iam:role"
    action: Mapped[str] = mapped_column(String(100)) # e.g. "s3:GetObject", "*"
    effect: Mapped[str] = mapped_column(String(50), default="ALLOW")
    
    is_admin_privilege: Mapped[bool] = mapped_column(Boolean, default=False)
    
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CiemIdentityRiskScore(Base):
    __tablename__ = "mf_ciem_risk_scores"
    """
    Dynamically calculated risk score of an identity.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_ciem_identities.id", ondelete="CASCADE"), index=True, unique=True)
    
    risk_score: Mapped[float] = mapped_column(Float, default=0.0) # 0.0 to 100.0
    risk_factors: Mapped[list] = mapped_column(JSON) # e.g. ["No MFA", "Admin Privilege", "Dormant"]
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AccessReview(Base):
    __tablename__ = "mf_ciem_access_reviews"
    """
    Governance records for periodic certification of role assignments.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    identity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_ciem_identities.id", ondelete="CASCADE"), index=True)
    
    reviewer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="PENDING") # PENDING, APPROVED, REVOKED
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
