import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class ForensicMobileDevice(Base):
    __tablename__ = "mf_mobile_devices"
    """
    Metadata about an acquired mobile device or backup (iOS/Android).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=True)
    
    device_name: Mapped[str] = mapped_column(String(255))
    os_type: Mapped[str] = mapped_column(String(50)) # iOS, Android
    os_version: Mapped[str] = mapped_column(String(50))
    acquisition_type: Mapped[str] = mapped_column(String(50)) # iTunes Backup, ADB Logical, Physical
    
    imei: Mapped[str] = mapped_column(String(50), nullable=True)
    
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    communications = relationship("ForensicMobileCommunication", back_populates="device", cascade="all, delete-orphan")
    locations = relationship("ForensicMobileLocation", back_populates="device", cascade="all, delete-orphan")


class ForensicMobileCommunication(Base):
    __tablename__ = "mf_mobile_communications"
    """
    Extracted messages (SMS, iMessage, WhatsApp).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    device_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_mobile_devices.id", ondelete="CASCADE"), index=True)
    
    app_name: Mapped[str] = mapped_column(String(100)) # Native SMS, WhatsApp, Signal
    thread_id: Mapped[str] = mapped_column(String(255), index=True)
    
    sender: Mapped[str] = mapped_column(String(255))
    receiver: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    is_outgoing: Mapped[bool] = mapped_column(Boolean)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    device = relationship("ForensicMobileDevice", back_populates="communications")


class ForensicMobileLocation(Base):
    __tablename__ = "mf_mobile_locations"
    """
    Extracted GPS coordinates, cell tower pings, or Wi-Fi connections.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    device_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_mobile_devices.id", ondelete="CASCADE"), index=True)
    
    source: Mapped[str] = mapped_column(String(100)) # GPS, CellTower, WiFi, EXIF
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    accuracy_meters: Mapped[float] = mapped_column(Float, nullable=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    device = relationship("ForensicMobileDevice", back_populates="locations")
