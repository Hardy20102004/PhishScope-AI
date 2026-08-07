import uuid
from typing import List

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


class NetworkInvestigation(Base):
    __tablename__ = "network_investigations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id = Column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Relationships
    flow_records = relationship("NetworkFlowRecord", back_populates="network_investigation", cascade="all, delete-orphan")
    dns_records = relationship("DNSRecord", back_populates="network_investigation", cascade="all, delete-orphan")
    http_metadata = relationship("HTTPMetadata", back_populates="network_investigation", cascade="all, delete-orphan")
    tls_metadata = relationship("TLSMetadata", back_populates="network_investigation", cascade="all, delete-orphan")
    timeline_events = relationship("NetworkTimelineEvent", back_populates="network_investigation", cascade="all, delete-orphan")
    extracted_iocs = relationship("ExtractedNetworkIOC", back_populates="network_investigation", cascade="all, delete-orphan")

class NetworkFlowRecord(Base):
    __tablename__ = "network_flow_records"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    network_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("network_investigations.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime(timezone=True))
    source_ip = Column(String, index=True)
    destination_ip = Column(String, index=True)
    source_port = Column(Integer)
    destination_port = Column(Integer)
    protocol = Column(String)
    bytes_sent = Column(Integer, default=0)
    bytes_received = Column(Integer, default=0)
    duration = Column(Float, default=0.0)
    
    network_investigation = relationship("NetworkInvestigation", back_populates="flow_records")

class DNSRecord(Base):
    __tablename__ = "network_dns_records"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    network_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("network_investigations.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime(timezone=True))
    query = Column(String, index=True)
    record_type = Column(String)
    response_code = Column(String)
    answers = Column(JSON, default=list) # List of resolved IPs or CNAMEs
    is_malicious = Column(Boolean, default=False)
    
    network_investigation = relationship("NetworkInvestigation", back_populates="dns_records")

class HTTPMetadata(Base):
    __tablename__ = "network_http_metadata"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    network_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("network_investigations.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime(timezone=True))
    method = Column(String)
    host = Column(String, index=True)
    uri = Column(Text)
    status_code = Column(Integer)
    user_agent = Column(Text)
    
    network_investigation = relationship("NetworkInvestigation", back_populates="http_metadata")

class TLSMetadata(Base):
    __tablename__ = "network_tls_metadata"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    network_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("network_investigations.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime(timezone=True))
    server_name = Column(String, index=True) # SNI
    version = Column(String)
    cipher = Column(String)
    ja3_fingerprint = Column(String, nullable=True)
    
    network_investigation = relationship("NetworkInvestigation", back_populates="tls_metadata")

class NetworkTimelineEvent(Base):
    __tablename__ = "network_timeline_events"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    network_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("network_investigations.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime(timezone=True), index=True)
    event_type = Column(String) # Flow, DNS, HTTP, TLS
    description = Column(String)
    source_table = Column(String)
    source_id = Column(String)
    
    network_investigation = relationship("NetworkInvestigation", back_populates="timeline_events")

class ExtractedNetworkIOC(Base):
    __tablename__ = "network_extracted_iocs"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    network_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("network_investigations.id", ondelete="CASCADE"), nullable=False)
    
    ioc_type = Column(String) # ip, domain, url
    ioc_value = Column(String)
    source_context = Column(String)
    
    network_investigation = relationship("NetworkInvestigation", back_populates="extracted_iocs")
