import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Uuid, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class EmailInvestigation(Base):
    __tablename__ = "email_investigations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id = Column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    subject = Column(String, index=True)
    message_id = Column(String, index=True)
    
    # Relationships
    header_data = relationship("EmailHeaderData", back_populates="email_investigation", uselist=False, cascade="all, delete-orphan")
    auth_results = relationship("AuthenticationResult", back_populates="email_investigation", uselist=False, cascade="all, delete-orphan")
    routing_hops = relationship("RoutingHop", back_populates="email_investigation", cascade="all, delete-orphan", order_by="RoutingHop.hop_index")
    attachments = relationship("AttachmentMetadata", back_populates="email_investigation", cascade="all, delete-orphan")
    extracted_urls = relationship("ExtractedURL", back_populates="email_investigation", cascade="all, delete-orphan")
    campaign = relationship("CampaignCorrelation", back_populates="email_investigation", uselist=False, cascade="all, delete-orphan")

class EmailHeaderData(Base):
    __tablename__ = "email_header_data"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("email_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    date_sent = Column(DateTime(timezone=True))
    sender_address = Column(String)
    return_path = Column(String)
    reply_to = Column(String)
    to_addresses = Column(JSON, default=list)
    cc_addresses = Column(JSON, default=list)
    
    raw_headers = Column(JSON, default=dict) # Store all parsed headers for UI
    
    email_investigation = relationship("EmailInvestigation", back_populates="header_data")

class AuthenticationResult(Base):
    __tablename__ = "authentication_results"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("email_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    spf_result = Column(String)
    dkim_result = Column(String)
    dmarc_result = Column(String)
    
    is_spoofed = Column(Boolean, default=False)
    
    email_investigation = relationship("EmailInvestigation", back_populates="auth_results")

class RoutingHop(Base):
    __tablename__ = "routing_hops"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("email_investigations.id", ondelete="CASCADE"), nullable=False)
    
    hop_index = Column(Integer)
    receiving_server = Column(String)
    sending_server = Column(String)
    sending_ip = Column(String)
    timestamp = Column(DateTime(timezone=True))
    latency_ms = Column(Float, nullable=True)
    
    email_investigation = relationship("EmailInvestigation", back_populates="routing_hops")

class AttachmentMetadata(Base):
    __tablename__ = "attachment_metadata"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("email_investigations.id", ondelete="CASCADE"), nullable=False)
    
    filename = Column(String)
    content_type = Column(String)
    size_bytes = Column(Integer)
    sha256_hash = Column(String, index=True)
    is_suspicious = Column(Boolean, default=False)
    
    email_investigation = relationship("EmailInvestigation", back_populates="attachments")

class ExtractedURL(Base):
    __tablename__ = "extracted_urls"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("email_investigations.id", ondelete="CASCADE"), nullable=False)
    
    url = Column(String)
    context = Column(String) # E.g., 'body', 'attachment_name.pdf'
    is_suspicious = Column(Boolean, default=False)
    
    email_investigation = relationship("EmailInvestigation", back_populates="extracted_urls")

class CampaignCorrelation(Base):
    __tablename__ = "campaign_correlations"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("email_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    campaign_name = Column(String)
    confidence_score = Column(Float)
    matched_indicators = Column(JSON, default=list)
    
    email_investigation = relationship("EmailInvestigation", back_populates="campaign")
