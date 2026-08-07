import uuid

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class MobileInvestigation(Base):
    __tablename__ = "mobile_investigations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id = Column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    device_name = Column(String, index=True)
    
    # Relationships
    device_metadata = relationship("DeviceMetadata", back_populates="mobile_investigation", uselist=False, cascade="all, delete-orphan")
    applications = relationship("MobileApplication", back_populates="mobile_investigation", cascade="all, delete-orphan")
    communications = relationship("MobileCommunication", back_populates="mobile_investigation", cascade="all, delete-orphan")
    locations = relationship("MobileLocation", back_populates="mobile_investigation", cascade="all, delete-orphan")
    timeline_events = relationship("MobileTimelineEvent", back_populates="mobile_investigation", cascade="all, delete-orphan")
    extracted_iocs = relationship("ExtractedMobileIOC", back_populates="mobile_investigation", cascade="all, delete-orphan")

class DeviceMetadata(Base):
    __tablename__ = "mobile_device_metadata"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mobile_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("mobile_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    manufacturer = Column(String)
    model = Column(String)
    os_name = Column(String) # Android, iOS
    os_version = Column(String)
    timezone = Column(String)
    
    mobile_investigation = relationship("MobileInvestigation", back_populates="device_metadata")

class MobileApplication(Base):
    __tablename__ = "mobile_applications"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mobile_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("mobile_investigations.id", ondelete="CASCADE"), nullable=False)
    
    app_name = Column(String)
    package_name = Column(String, index=True)
    version = Column(String)
    permissions = Column(JSON, default=list)
    is_suspicious = Column(Boolean, default=False)
    
    mobile_investigation = relationship("MobileInvestigation", back_populates="applications")

class MobileCommunication(Base):
    __tablename__ = "mobile_communications"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mobile_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("mobile_investigations.id", ondelete="CASCADE"), nullable=False)
    
    comm_type = Column(String) # SMS, Call, WhatsApp
    direction = Column(String) # Incoming, Outgoing
    contact_name = Column(String, nullable=True)
    contact_number = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True))
    body = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    mobile_investigation = relationship("MobileInvestigation", back_populates="communications")

class MobileLocation(Base):
    __tablename__ = "mobile_locations"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mobile_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("mobile_investigations.id", ondelete="CASCADE"), nullable=False)
    
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    source = Column(String) # GPS, Network, Wi-Fi
    label = Column(String, nullable=True)
    
    mobile_investigation = relationship("MobileInvestigation", back_populates="locations")

class MobileTimelineEvent(Base):
    __tablename__ = "mobile_timeline_events"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mobile_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("mobile_investigations.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime(timezone=True), index=True)
    event_type = Column(String) # AppInstall, SMS, Call, LocationUpdate
    description = Column(String)
    source_table = Column(String)
    source_id = Column(String)
    
    mobile_investigation = relationship("MobileInvestigation", back_populates="timeline_events")

class ExtractedMobileIOC(Base):
    __tablename__ = "mobile_extracted_iocs"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mobile_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("mobile_investigations.id", ondelete="CASCADE"), nullable=False)
    
    ioc_type = Column(String) # url, phone_number, ip
    ioc_value = Column(String)
    source_context = Column(String) # 'SMS from +12345'
    
    mobile_investigation = relationship("MobileInvestigation", back_populates="extracted_iocs")
