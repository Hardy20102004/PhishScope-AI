import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
import enum

class IOCType(str, enum.Enum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"
    DOMAIN = "Domain"
    SUBDOMAIN = "Subdomain"
    URL = "URL"
    EMAIL = "Email Address"
    PHONE = "Phone Number"
    SHA256 = "SHA256"
    SHA1 = "SHA1"
    MD5 = "MD5"
    TLS_CERT = "TLS Certificate"
    JA3 = "JA3 Fingerprint"
    JA4 = "JA4 Fingerprint"
    FILE_NAME = "File Name"
    WALLET = "Wallet Address"
    CLOUD_RESOURCE = "Cloud Resource ID"
    APK_PACKAGE = "Android Package Name"
    BROWSER_EXT = "Browser Extension"
    YARA = "YARA Rule ID"
    SIGMA = "Sigma Rule ID"
    MITRE_TECHNIQUE = "MITRE ATT&CK Technique"
    CUSTOM = "Custom Enterprise Indicator"

class RelationshipType(str, enum.Enum):
    EXACT_MATCH = "Exact Match"
    SHARED_INFRASTRUCTURE = "Infrastructure Sharing"
    SHARED_CERTIFICATE = "Certificate Sharing"
    SHARED_DOMAIN = "Shared Domain"
    SHARED_IP = "Shared IP"
    SHARED_URL = "Shared URL"
    SHARED_EMAIL = "Shared Email"
    SHARED_WALLET = "Shared Wallet"
    SHARED_CLOUD_RESOURCE = "Shared Cloud Resource"
    SHARED_APK = "Shared APK"
    SHARED_MALWARE_FAMILY = "Shared Malware Family"
    SHARED_CAMPAIGN = "Shared Campaign"
    HISTORICAL = "Historical Relationship"


class Indicator(Base):
    __tablename__ = "indicator"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    value: Mapped[str] = mapped_column(String, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String, index=True, nullable=False) # Will store IOCType values
    normalized_value: Mapped[str] = mapped_column(String, index=True, nullable=False)
    
    # Computed reputation from feeds
    reputation_score: Mapped[float] = mapped_column(Float, default=0.0) # 0 to 100
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0) # 0 to 100
    threat_classification: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Phishing, Malware, etc.
    
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    observation_count: Mapped[int] = mapped_column(Integer, default=1)
    
    # New Enterprise Engine Fields
    source_module: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    raw_context: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    normalization_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    feed_results: Mapped[List["ThreatFeedResult"]] = relationship("ThreatFeedResult", back_populates="indicator", cascade="all, delete-orphan")


class ThreatFeedResult(Base):
    __tablename__ = "threat_feed_result"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    indicator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("indicator.id", ondelete="CASCADE"), index=True)
    source: Mapped[str] = mapped_column(String, index=True, nullable=False) # virustotal, google_safe_browsing, etc.
    
    reputation_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    threat_classification: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    raw_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True) # Full response from the feed
    is_cached: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    indicator: Mapped["Indicator"] = relationship("Indicator", back_populates="feed_results")

# For keeping track of related indicators
class IndicatorCorrelation(Base):
    __tablename__ = "indicator_correlation"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_indicator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("indicator.id", ondelete="CASCADE"), index=True)
    target_indicator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("indicator.id", ondelete="CASCADE"), index=True)
    correlation_type: Mapped[str] = mapped_column(String, nullable=False) # e.g., "resolves_to", "same_certificate", "related_email"
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Enterprise Fields
    similarity_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

class CorrelationEvidence(Base):
    __tablename__ = "correlation_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    relationship_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("indicator_correlation.id", ondelete="CASCADE"), index=True)
    
    evidence_type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    evidence_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    source_system: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class IndicatorRisk(Base):
    __tablename__ = "indicator_risk"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    indicator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("indicator.id", ondelete="CASCADE"), unique=True)
    
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_level: Mapped[float] = mapped_column(Float, default=0.0)
    uncertainty: Mapped[float] = mapped_column(Float, default=0.0)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    
    threat_actor: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    campaign: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
