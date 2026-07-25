import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Indicator(Base):
    __tablename__ = "indicator"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    value: Mapped[str] = mapped_column(String, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String, index=True, nullable=False) # url, domain, ipv4, ipv6, email, sha256, etc.
    normalized_value: Mapped[str] = mapped_column(String, index=True, nullable=False)
    
    # Computed reputation from feeds
    reputation_score: Mapped[float] = mapped_column(Float, default=0.0) # 0 to 100
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0) # 0 to 100
    threat_classification: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Phishing, Malware, etc.
    
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    observation_count: Mapped[int] = mapped_column(Integer, default=1)
    
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
