import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class UnifiedCloudAsset(Base):
    __tablename__ = "mf_mc_unified_assets"
    """
    A normalized representation of any cloud entity (VM, Bucket, IAM Role).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    asset_name: Mapped[str] = mapped_column(String(255))
    provider: Mapped[str] = mapped_column(String(50)) # AWS, AZURE, GCP, K8S
    asset_type: Mapped[str] = mapped_column(String(100)) # COMPUTE, STORAGE, IDENTITY, NETWORK
    environment: Mapped[str] = mapped_column(String(50)) # PROD, STAGING, DEV
    
    native_id: Mapped[str] = mapped_column(String(255)) # Original ARN, Resource ID, etc.
    tags: Mapped[dict] = mapped_column(JSON, default=dict)
    
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CrossCloudRelationship(Base):
    __tablename__ = "mf_mc_relationships"
    """
    Maps connections between assets across different clouds.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    source_asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_mc_unified_assets.id", ondelete="CASCADE"), index=True)
    target_asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_mc_unified_assets.id", ondelete="CASCADE"), index=True)
    
    relationship_type: Mapped[str] = mapped_column(String(100)) # e.g. "AUTHENTICATES_TO", "STORES_DATA_IN", "COMMUNICATES_WITH"
    
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class UnifiedRiskScore(Base):
    __tablename__ = "mf_mc_risk_scores"
    """
    The aggregated risk score calculated for the entire enterprise cloud estate.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    global_score: Mapped[float] = mapped_column(Float, default=0.0) # 0 to 1000
    provider_breakdown: Mapped[dict] = mapped_column(JSON, default=dict) # {"AWS": 450, "AZURE": 200, "GCP": 100}
    category_breakdown: Mapped[dict] = mapped_column(JSON, default=dict) # {"CSPM": 300, "CWPP": 200, "CIEM": 250}
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ComplianceTrend(Base):
    __tablename__ = "mf_mc_compliance_trends"
    """
    Historical tracking of compliance framework alignment.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    framework: Mapped[str] = mapped_column(String(100)) # NIST_CSF, CIS_CONTROLS, ISO_27001
    compliance_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    failed_controls: Mapped[int] = mapped_column(Integer, default=0)
    
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
