import uuid

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Uuid,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CloudInvestigation(Base):
    __tablename__ = "cloud_investigations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id = Column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    cloud_provider = Column(String, index=True) # AWS, GCP, Azure
    
    # Relationships
    assets = relationship("CloudAsset", back_populates="cloud_investigation", cascade="all, delete-orphan")
    identities = relationship("CloudIdentity", back_populates="cloud_investigation", cascade="all, delete-orphan")
    configurations = relationship("CloudConfiguration", back_populates="cloud_investigation", cascade="all, delete-orphan")
    audit_events = relationship("CloudAuditEvent", back_populates="cloud_investigation", cascade="all, delete-orphan")
    timeline_events = relationship("CloudTimelineEvent", back_populates="cloud_investigation", cascade="all, delete-orphan")
    extracted_iocs = relationship("ExtractedCloudIOC", back_populates="cloud_investigation", cascade="all, delete-orphan")

class CloudAsset(Base):
    __tablename__ = "cloud_assets"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cloud_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("cloud_investigations.id", ondelete="CASCADE"), nullable=False)
    
    asset_type = Column(String, index=True) # EC2, S3, IAM, etc.
    asset_id = Column(String, index=True)
    name = Column(String)
    region = Column(String)
    is_public = Column(Boolean, default=False)
    metadata_json = Column(JSON, default=dict)
    
    cloud_investigation = relationship("CloudInvestigation", back_populates="assets")

class CloudIdentity(Base):
    __tablename__ = "cloud_identities"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cloud_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("cloud_investigations.id", ondelete="CASCADE"), nullable=False)
    
    identity_type = Column(String) # User, Role, Group
    identity_id = Column(String, index=True)
    name = Column(String)
    permissions = Column(JSON, default=list)
    is_highly_privileged = Column(Boolean, default=False)
    
    cloud_investigation = relationship("CloudInvestigation", back_populates="identities")

class CloudConfiguration(Base):
    __tablename__ = "cloud_configurations"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cloud_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("cloud_investigations.id", ondelete="CASCADE"), nullable=False)
    
    config_type = Column(String) # IAM Policy, Bucket Policy, Security Group
    resource_id = Column(String, index=True)
    details = Column(JSON, default=dict)
    is_misconfigured = Column(Boolean, default=False)
    
    cloud_investigation = relationship("CloudInvestigation", back_populates="configurations")

class CloudAuditEvent(Base):
    __tablename__ = "cloud_audit_events"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cloud_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("cloud_investigations.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime(timezone=True), index=True)
    event_name = Column(String, index=True)
    event_source = Column(String)
    actor = Column(String)
    source_ip = Column(String)
    user_agent = Column(String)
    is_anomalous = Column(Boolean, default=False)
    
    cloud_investigation = relationship("CloudInvestigation", back_populates="audit_events")

class CloudTimelineEvent(Base):
    __tablename__ = "cloud_timeline_events"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cloud_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("cloud_investigations.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime(timezone=True), index=True)
    event_type = Column(String) # Audit, ConfigChange, AssetCreation
    description = Column(String)
    source_table = Column(String)
    source_id = Column(String)
    
    cloud_investigation = relationship("CloudInvestigation", back_populates="timeline_events")

class ExtractedCloudIOC(Base):
    __tablename__ = "cloud_extracted_iocs"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cloud_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("cloud_investigations.id", ondelete="CASCADE"), nullable=False)
    
    ioc_type = Column(String) # ip, domain, cloud_id
    ioc_value = Column(String)
    source_context = Column(String)
    
    cloud_investigation = relationship("CloudInvestigation", back_populates="extracted_iocs")
