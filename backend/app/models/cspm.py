import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class CSPMCloudAsset(Base):
    __tablename__ = "mf_cspm_assets"
    """
    Represents discovered multi-cloud resources.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    provider: Mapped[str] = mapped_column(String(50)) # AWS, GCP, AZURE
    asset_type: Mapped[str] = mapped_column(String(100)) # COMPUTE, STORAGE, IAM, NETWORK
    asset_name: Mapped[str] = mapped_column(String(255))
    region: Mapped[str] = mapped_column(String(100))
    
    configuration: Mapped[dict] = mapped_column(JSON, default=dict)
    
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CloudMisconfiguration(Base):
    __tablename__ = "mf_cspm_misconfigurations"
    """
    Specific security risks identified on a cloud asset.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_cspm_assets.id", ondelete="CASCADE"))
    
    title: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(String(50)) # CRITICAL, HIGH, MEDIUM, LOW
    description: Mapped[str] = mapped_column(Text)
    remediation_steps: Mapped[str] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(50), default="OPEN") # OPEN, RESOLVED, ACCEPTED
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ComplianceFinding(Base):
    __tablename__ = "mf_cspm_compliance"
    """
    Results of evaluating an asset against a specific framework.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    framework: Mapped[str] = mapped_column(String(100)) # CIS_AWS_v1.4, NIST_800_53
    control_id: Mapped[str] = mapped_column(String(100))
    
    passed: Mapped[int] = mapped_column(Integer, default=0)
    failed: Mapped[int] = mapped_column(Integer, default=0)
    
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
