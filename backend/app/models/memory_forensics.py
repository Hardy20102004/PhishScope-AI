import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class MemoryImage(Base):
    __tablename__ = "mf_memory_images"
    """
    Metadata about an uploaded volatile memory dump (RAW, vmem, etc).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=True)
    
    filename: Mapped[str] = mapped_column(String(255))
    os_profile: Mapped[str] = mapped_column(String(100)) # e.g., Win10x64_19041
    size_bytes: Mapped[int] = mapped_column(Integer)
    
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    processes = relationship("MemoryProcess", back_populates="memory_image", cascade="all, delete-orphan")
    network_connections = relationship("MemoryNetworkConnection", back_populates="memory_image", cascade="all, delete-orphan")


class MemoryProcess(Base):
    __tablename__ = "mf_memory_processes"
    """
    Extracted process objects (EPROCESS structures) from RAM.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    memory_image_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_memory_images.id", ondelete="CASCADE"), index=True)
    
    pid: Mapped[int] = mapped_column(Integer, index=True)
    ppid: Mapped[int] = mapped_column(Integer, index=True)
    name: Mapped[str] = mapped_column(String(255))
    
    # Forensic Flags
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False) # Unlinked from process active head (DKOM)
    is_injected: Mapped[bool] = mapped_column(Boolean, default=False) # Hollowed or anomalous memory regions
    
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    memory_image = relationship("MemoryImage", back_populates="processes")


class MemoryNetworkConnection(Base):
    __tablename__ = "mf_memory_network_connections"
    """
    Active or listening network sockets extracted from memory structures.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    memory_image_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_memory_images.id", ondelete="CASCADE"), index=True)
    pid: Mapped[int] = mapped_column(Integer, nullable=True) # Linked process if available
    
    protocol: Mapped[str] = mapped_column(String(10)) # TCP, UDP
    local_ip: Mapped[str] = mapped_column(String(45))
    local_port: Mapped[int] = mapped_column(Integer)
    remote_ip: Mapped[str] = mapped_column(String(45))
    remote_port: Mapped[int] = mapped_column(Integer)
    
    state: Mapped[str] = mapped_column(String(50)) # ESTABLISHED, LISTENING, CLOSED
    
    memory_image = relationship("MemoryImage", back_populates="network_connections")
