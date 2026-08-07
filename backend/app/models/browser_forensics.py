import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class BrowserProfile(Base):
    __tablename__ = "mf_browser_profiles"
    """
    Metadata about an acquired browser profile (e.g. Chrome Default Profile).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=True)
    
    browser_type: Mapped[str] = mapped_column(String(50)) # Chrome, Edge, Firefox
    profile_name: Mapped[str] = mapped_column(String(255))
    host_os: Mapped[str] = mapped_column(String(50))
    
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    history_records = relationship("BrowserHistory", back_populates="profile", cascade="all, delete-orphan")
    extensions = relationship("ForensicBrowserExtension", back_populates="profile", cascade="all, delete-orphan")


class BrowserHistory(Base):
    __tablename__ = "mf_browser_history"
    """
    Extracted web browsing history URLs.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_browser_profiles.id", ondelete="CASCADE"), index=True)
    
    url: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text, nullable=True)
    visit_count: Mapped[int] = mapped_column(Integer, default=1)
    
    is_threat_hit: Mapped[bool] = mapped_column(Boolean, default=False)
    threat_category: Mapped[str] = mapped_column(String(100), nullable=True) # e.g. Phishing, C2
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    profile = relationship("BrowserProfile", back_populates="history_records")


class ForensicBrowserExtension(Base):
    __tablename__ = "mf_browser_extensions"
    """
    Installed browser extensions/plugins.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    profile_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_browser_profiles.id", ondelete="CASCADE"), index=True)
    
    extension_id: Mapped[str] = mapped_column(String(100), index=True)
    name: Mapped[str] = mapped_column(String(255))
    version: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Comma-separated list of permissions (e.g. "tabs, <all_urls>, storage")
    permissions: Mapped[str] = mapped_column(Text, nullable=True)
    
    is_suspicious: Mapped[bool] = mapped_column(Boolean, default=False)
    
    install_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    profile = relationship("BrowserProfile", back_populates="extensions")
