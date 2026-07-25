import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Uuid, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class WebsiteInvestigation(Base):
    __tablename__ = "website_investigations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id = Column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    url = Column(String, index=True)
    
    # Relationships
    page_snapshot = relationship("PageSnapshot", back_populates="website_investigation", uselist=False, cascade="all, delete-orphan")
    js_metadata = relationship("JavaScriptMetadata", back_populates="website_investigation", cascade="all, delete-orphan")
    form_metadata = relationship("FormMetadata", back_populates="website_investigation", cascade="all, delete-orphan")
    security_headers = relationship("SecurityHeaderData", back_populates="website_investigation", uselist=False, cascade="all, delete-orphan")
    visual_analysis = relationship("VisualAnalysisData", back_populates="website_investigation", uselist=False, cascade="all, delete-orphan")

class PageSnapshot(Base):
    __tablename__ = "page_snapshots"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    website_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("website_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    title = Column(String)
    description = Column(String)
    language = Column(String)
    has_hidden_elements = Column(Boolean, default=False)
    has_iframes = Column(Boolean, default=False)
    has_meta_refresh = Column(Boolean, default=False)
    has_suspicious_tags = Column(Boolean, default=False)
    embedded_credentials = Column(Boolean, default=False)
    
    cookies = Column(JSON, default=list) # Store cookie metadata here for simplicity
    
    website_investigation = relationship("WebsiteInvestigation", back_populates="page_snapshot")

class JavaScriptMetadata(Base):
    __tablename__ = "javascript_metadata"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    website_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("website_investigations.id", ondelete="CASCADE"), nullable=False)
    
    script_source = Column(String) # URL or 'inline'
    is_obfuscated = Column(Boolean, default=False)
    makes_ajax_requests = Column(Boolean, default=False)
    accesses_clipboard = Column(Boolean, default=False)
    uses_suspicious_apis = Column(Boolean, default=False)
    is_tracking_library = Column(Boolean, default=False)
    
    website_investigation = relationship("WebsiteInvestigation", back_populates="js_metadata")

class FormMetadata(Base):
    __tablename__ = "form_metadata"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    website_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("website_investigations.id", ondelete="CASCADE"), nullable=False)
    
    action_url = Column(String)
    is_login = Column(Boolean, default=False)
    has_password_field = Column(Boolean, default=False)
    has_credit_card_field = Column(Boolean, default=False)
    requests_personal_info = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    
    website_investigation = relationship("WebsiteInvestigation", back_populates="form_metadata")

class SecurityHeaderData(Base):
    __tablename__ = "security_header_data"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    website_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("website_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    content_security_policy = Column(String)
    strict_transport_security = Column(String)
    x_frame_options = Column(String)
    x_content_type_options = Column(String)
    referrer_policy = Column(String)
    permissions_policy = Column(String)
    has_mixed_content = Column(Boolean, default=False)
    
    website_investigation = relationship("WebsiteInvestigation", back_populates="security_headers")

class VisualAnalysisData(Base):
    __tablename__ = "visual_analysis_data"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    website_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("website_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    screenshot_path = Column(String) # Path to stored screenshot
    impersonates_brand = Column(Boolean, default=False)
    brand_name = Column(String)
    similarity_score = Column(Float)
    is_fake_login = Column(Boolean, default=False)
    is_fake_banking = Column(Boolean, default=False)
    
    website_investigation = relationship("WebsiteInvestigation", back_populates="visual_analysis")
