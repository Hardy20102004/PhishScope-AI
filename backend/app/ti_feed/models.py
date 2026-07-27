import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base

class FeedStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ERROR = "Error"
    SYNCING = "Syncing"

class FeedFormat(str, enum.Enum):
    STIX_21 = "STIX 2.1"
    TAXII = "TAXII"
    MISP = "MISP"
    OPENCTI = "OpenCTI"
    CSV = "CSV"
    JSON = "JSON"

class FeedType(str, enum.Enum):
    INTERNAL = "Internal Intelligence"
    COMMERCIAL = "Commercial Threat Intelligence"
    COMMUNITY = "Community Intelligence"
    OSINT = "Open Source Intelligence"

class FeedRegistry(Base):
    __tablename__ = "ti_feed_registry"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    feed_type: Mapped[FeedType] = mapped_column(Enum(FeedType), nullable=False)
    format: Mapped[FeedFormat] = mapped_column(Enum(FeedFormat), nullable=False)
    source_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    
    auth_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True) # Encrypted credentials ideally
    connector_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True) # e.g. CSV column mappings
    
    sync_interval_minutes: Mapped[int] = mapped_column(Integer, default=60)
    status: Mapped[FeedStatus] = mapped_column(Enum(FeedStatus), default=FeedStatus.INACTIVE)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    last_sync_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_sync_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    versions: Mapped[List["FeedVersion"]] = relationship("FeedVersion", back_populates="feed", cascade="all, delete-orphan")


class SyncStatus(str, enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    PARTIAL = "Completed with Errors"
    FAILED = "Failed"

class FeedVersion(Base):
    """
    Maintains versions/history of feed synchronization.
    """
    __tablename__ = "ti_feed_version"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feed_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("ti_feed_registry.id", ondelete="CASCADE"), index=True)
    
    version_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[SyncStatus] = mapped_column(Enum(SyncStatus), default=SyncStatus.PENDING)
    
    indicators_added: Mapped[int] = mapped_column(Integer, default=0)
    indicators_updated: Mapped[int] = mapped_column(Integer, default=0)
    errors_encountered: Mapped[int] = mapped_column(Integer, default=0)
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    feed: Mapped["FeedRegistry"] = relationship("FeedRegistry", back_populates="versions")

class FeedIndicator(Base):
    """
    Links a raw feed entry to the central IOC Correlation Engine's Indicator table.
    """
    __tablename__ = "ti_feed_indicator"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feed_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("ti_feed_registry.id", ondelete="CASCADE"), index=True)
    version_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("ti_feed_version.id", ondelete="CASCADE"), index=True)
    
    # Links to the central threat_intel.Indicator
    global_indicator_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("indicator.id", ondelete="SET NULL"), index=True)
    
    raw_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False) # The original STIX/JSON object
    validation_status: Mapped[str] = mapped_column(String(50), default="Valid")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class FeedAuditLog(Base):
    __tablename__ = "ti_feed_audit_log"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feed_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("ti_feed_registry.id", ondelete="CASCADE"), index=True)
    version_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("ti_feed_version.id", ondelete="SET NULL"))
    
    level: Mapped[str] = mapped_column(String(50), nullable=False) # INFO, WARNING, ERROR
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
