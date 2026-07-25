import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Uuid, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class BrowserInvestigation(Base):
    __tablename__ = "browser_investigations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id = Column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    browser_type = Column(String, index=True) # Chrome, Firefox
    
    # Relationships
    history_records = relationship("BrowserHistoryRecord", back_populates="browser_investigation", cascade="all, delete-orphan")
    cookies = relationship("BrowserCookie", back_populates="browser_investigation", cascade="all, delete-orphan")
    extensions = relationship("BrowserExtension", back_populates="browser_investigation", cascade="all, delete-orphan")
    downloads = relationship("BrowserDownload", back_populates="browser_investigation", cascade="all, delete-orphan")
    timeline_events = relationship("BrowserTimelineEvent", back_populates="browser_investigation", cascade="all, delete-orphan")
    extracted_iocs = relationship("ExtractedBrowserIOC", back_populates="browser_investigation", cascade="all, delete-orphan")

class BrowserHistoryRecord(Base):
    __tablename__ = "browser_history_records"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    browser_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("browser_investigations.id", ondelete="CASCADE"), nullable=False)
    
    url = Column(Text, index=True)
    title = Column(String, nullable=True)
    visit_time = Column(DateTime(timezone=True))
    visit_count = Column(Integer, default=1)
    is_search = Column(Boolean, default=False)
    search_keyword = Column(String, nullable=True)
    
    browser_investigation = relationship("BrowserInvestigation", back_populates="history_records")

class BrowserCookie(Base):
    __tablename__ = "browser_cookies"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    browser_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("browser_investigations.id", ondelete="CASCADE"), nullable=False)
    
    domain = Column(String, index=True)
    name = Column(String)
    creation_time = Column(DateTime(timezone=True))
    expiration_time = Column(DateTime(timezone=True), nullable=True)
    is_secure = Column(Boolean, default=False)
    is_httponly = Column(Boolean, default=False)
    
    browser_investigation = relationship("BrowserInvestigation", back_populates="cookies")

class BrowserExtension(Base):
    __tablename__ = "browser_extensions"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    browser_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("browser_investigations.id", ondelete="CASCADE"), nullable=False)
    
    extension_id = Column(String, index=True)
    name = Column(String)
    version = Column(String)
    permissions = Column(JSON, default=list)
    is_suspicious = Column(Boolean, default=False)
    
    browser_investigation = relationship("BrowserInvestigation", back_populates="extensions")

class BrowserDownload(Base):
    __tablename__ = "browser_downloads"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    browser_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("browser_investigations.id", ondelete="CASCADE"), nullable=False)
    
    filename = Column(String)
    source_url = Column(Text)
    download_time = Column(DateTime(timezone=True))
    file_size = Column(Integer)
    is_malicious = Column(Boolean, default=False)
    
    browser_investigation = relationship("BrowserInvestigation", back_populates="downloads")

class BrowserTimelineEvent(Base):
    __tablename__ = "browser_timeline_events"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    browser_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("browser_investigations.id", ondelete="CASCADE"), nullable=False)
    
    timestamp = Column(DateTime(timezone=True), index=True)
    event_type = Column(String) # Visit, Search, Download, CookieCreated
    description = Column(String)
    source_table = Column(String)
    source_id = Column(String)
    
    browser_investigation = relationship("BrowserInvestigation", back_populates="timeline_events")

class ExtractedBrowserIOC(Base):
    __tablename__ = "browser_extracted_iocs"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    browser_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("browser_investigations.id", ondelete="CASCADE"), nullable=False)
    
    ioc_type = Column(String) # url, domain, search_keyword
    ioc_value = Column(String)
    source_context = Column(String)
    
    browser_investigation = relationship("BrowserInvestigation", back_populates="extracted_iocs")
