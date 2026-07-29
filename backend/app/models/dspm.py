import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class CloudDataAsset(Base):
    __tablename__ = "mf_dspm_data_assets"
    """
    Inventory of discovered data stores (S3 buckets, RDS instances, etc.).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    asset_name: Mapped[str] = mapped_column(String(255))
    provider: Mapped[str] = mapped_column(String(50)) # AWS, AZURE, GCP
    service_type: Mapped[str] = mapped_column(String(100)) # S3, RDS, BigQuery
    location: Mapped[str] = mapped_column(String(100)) # us-east-1
    
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_encrypted: Mapped[bool] = mapped_column(Boolean, default=False)
    encryption_type: Mapped[str] = mapped_column(String(50), nullable=True) # AWS_MANAGED, CUSTOMER_MANAGED
    
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DataClassification(Base):
    __tablename__ = "mf_dspm_classifications"
    """
    Assigned sensitivity labels linked to a data asset.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_dspm_data_assets.id", ondelete="CASCADE"), index=True)
    
    label: Mapped[str] = mapped_column(String(100)) # PII, PHI, FINANCIAL, PUBLIC
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    requires_review: Mapped[bool] = mapped_column(Boolean, default=False)
    
    classified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DataExposureFinding(Base):
    __tablename__ = "mf_dspm_exposure_findings"
    """
    Specific risks identified for a data asset.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_dspm_data_assets.id", ondelete="CASCADE"), index=True)
    
    finding_type: Mapped[str] = mapped_column(String(100)) # e.g., PUBLIC_ACCESS, CROSS_ACCOUNT_SHARING
    severity: Mapped[str] = mapped_column(String(50)) # CRITICAL, HIGH, MEDIUM, LOW
    description: Mapped[str] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(50), default="OPEN") # OPEN, RESOLVED, EXCEPTED
    
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DataAccessGovernance(Base):
    __tablename__ = "mf_dspm_access_governance"
    """
    Analysis of identities possessing access to sensitive data assets.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_dspm_data_assets.id", ondelete="CASCADE"), index=True)
    principal_id: Mapped[str] = mapped_column(String(255))
    
    access_level: Mapped[str] = mapped_column(String(50)) # READ, WRITE, ADMIN
    last_accessed: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_dormant: Mapped[bool] = mapped_column(Boolean, default=False)
    
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
