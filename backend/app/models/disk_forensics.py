import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class DiskImage(Base):
    __tablename__ = "df_disk_images"
    """
    Metadata about an uploaded forensic disk image (E01, RAW, etc).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=True)
    
    filename: Mapped[str] = mapped_column(String(255))
    format: Mapped[str] = mapped_column(String(50)) # E01, RAW, VMDK
    size_bytes: Mapped[int] = mapped_column(Integer)
    
    md5_hash: Mapped[str] = mapped_column(String(32))
    sha256_hash: Mapped[str] = mapped_column(String(64))
    hash_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    partitions = relationship("DiskPartition", back_populates="disk_image", cascade="all, delete-orphan")


class DiskPartition(Base):
    __tablename__ = "df_disk_partitions"
    """
    Parsed volumes/partitions from a disk image.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    disk_image_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("df_disk_images.id", ondelete="CASCADE"), index=True)
    
    partition_type: Mapped[str] = mapped_column(String(50)) # NTFS, EXT4, APFS
    start_sector: Mapped[int] = mapped_column(Integer)
    size_bytes: Mapped[int] = mapped_column(Integer)
    
    disk_image = relationship("DiskImage", back_populates="partitions")
    artifacts = relationship("ForensicArtifact", back_populates="partition", cascade="all, delete-orphan")


class ForensicArtifact(Base):
    __tablename__ = "df_forensic_artifacts"
    """
    Files or carved data extracted from a partition.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    partition_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("df_disk_partitions.id", ondelete="CASCADE"), index=True)
    
    filepath: Mapped[str] = mapped_column(Text)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_carved: Mapped[bool] = mapped_column(Boolean, default=False) # True if recovered from unallocated space
    
    # MAC Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    partition = relationship("DiskPartition", back_populates="artifacts")
