import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum, JSON, Uuid, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class URLInvestigationDetails(Base):
    """Detailed structured data for URL investigations."""
    __tablename__ = "url_investigation_details"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id = Column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # URL Features
    url_length = Column(Integer)
    entropy = Column(Float)
    suspicious_keywords_found = Column(JSON, default=list) # List of keywords
    
    # Normalization
    canonical_url = Column(String, index=True)
    
    # Relationships
    parsed_url = relationship("ParsedURL", back_populates="investigation_details", uselist=False, cascade="all, delete-orphan")
    redirect_chain = relationship("RedirectChain", back_populates="investigation_details", cascade="all, delete-orphan")
    infrastructure = relationship("DomainInfrastructure", back_populates="investigation_details", uselist=False, cascade="all, delete-orphan")
    brand_intelligence = relationship("BrandIntelligence", back_populates="investigation_details", uselist=False, cascade="all, delete-orphan")

class ParsedURL(Base):
    __tablename__ = "parsed_urls"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    url_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("url_investigation_details.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    protocol = Column(String)
    hostname = Column(String, index=True)
    subdomain = Column(String)
    root_domain = Column(String, index=True)
    public_suffix = Column(String)
    port = Column(Integer)
    path = Column(String)
    query_parameters = Column(JSON, default=dict)
    fragments = Column(String)
    encoded_characters = Column(Boolean, default=False)
    unicode_characters = Column(Boolean, default=False)
    
    investigation_details = relationship("URLInvestigationDetails", back_populates="parsed_url")

class RedirectChain(Base):
    __tablename__ = "redirect_chains"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    url_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("url_investigation_details.id", ondelete="CASCADE"), nullable=False)
    
    step_index = Column(Integer, nullable=False)
    from_url = Column(String, nullable=False)
    to_url = Column(String, nullable=False)
    status_code = Column(Integer)
    redirect_type = Column(String) # HTTP, Meta, JS
    response_time_ms = Column(Float)
    
    investigation_details = relationship("URLInvestigationDetails", back_populates="redirect_chain")

class DomainInfrastructure(Base):
    __tablename__ = "domain_infrastructures"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    url_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("url_investigation_details.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    domain_name = Column(String, index=True, nullable=False)
    ips = Column(JSON, default=list) # List of IPs
    asn = Column(String)
    asn_org = Column(String)
    nameservers = Column(JSON, default=list)
    mx_records = Column(JSON, default=list)
    txt_records = Column(JSON, default=list)
    
    whois_registrar = Column(String)
    whois_creation_date = Column(DateTime(timezone=True))
    whois_expiration_date = Column(DateTime(timezone=True))
    
    certificates = relationship("CertificateData", back_populates="infrastructure", cascade="all, delete-orphan")
    investigation_details = relationship("URLInvestigationDetails", back_populates="infrastructure")

class CertificateData(Base):
    __tablename__ = "certificate_data"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    infrastructure_id = Column(Uuid(as_uuid=True), ForeignKey("domain_infrastructures.id", ondelete="CASCADE"), nullable=False)
    
    issuer = Column(String)
    subject = Column(String)
    valid_from = Column(DateTime(timezone=True))
    valid_to = Column(DateTime(timezone=True))
    subject_alt_names = Column(JSON, default=list)
    tls_version = Column(String)
    is_valid = Column(Boolean)
    
    infrastructure = relationship("DomainInfrastructure", back_populates="certificates")

class BrandIntelligence(Base):
    __tablename__ = "brand_intelligence"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    url_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("url_investigation_details.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    is_typosquat = Column(Boolean, default=False)
    typosquat_target = Column(String)
    is_homograph = Column(Boolean, default=False)
    homograph_target = Column(String)
    brand_impersonation_score = Column(Float)
    targeted_brand = Column(String)
    
    investigation_details = relationship("URLInvestigationDetails", back_populates="brand_intelligence")
