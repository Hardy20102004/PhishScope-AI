import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Text, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base

class CampaignStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    EMERGING = "Emerging"
    UNKNOWN = "Unknown"

class CampaignSeverity(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Campaign(Base):
    __tablename__ = "campaign_registry"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    aliases: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    status: Mapped[CampaignStatus] = mapped_column(Enum(CampaignStatus), default=CampaignStatus.EMERGING)
    severity: Mapped[CampaignSeverity] = mapped_column(Enum(CampaignSeverity), default=CampaignSeverity.MEDIUM)
    confidence: Mapped[float] = mapped_column(Float, default=0.0) # Confidence in the clustering/attribution
    
    first_observed: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_observed: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    infrastructure: Mapped[List["CampaignInfrastructure"]] = relationship("CampaignInfrastructure", back_populates="campaign", cascade="all, delete-orphan")
    victims: Mapped[List["CampaignVictim"]] = relationship("CampaignVictim", back_populates="campaign", cascade="all, delete-orphan")
    timeline_events: Mapped[List["CampaignTimeline"]] = relationship("CampaignTimeline", back_populates="campaign", cascade="all, delete-orphan")
    evidence: Mapped[List["CampaignEvidence"]] = relationship("CampaignEvidence", back_populates="campaign", cascade="all, delete-orphan")

class CampaignInfrastructure(Base):
    """
    Links a campaign to an underlying IOC (IP, Domain, Hash)
    """
    __tablename__ = "campaign_infrastructure"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("campaign_registry.id", ondelete="CASCADE"), index=True)
    indicator_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("indicator.id", ondelete="CASCADE"), index=True)
    
    usage: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # e.g., "C2", "Payload Delivery"
    first_seen: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_seen: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="infrastructure")

class CampaignVictim(Base):
    __tablename__ = "campaign_victims"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("campaign_registry.id", ondelete="CASCADE"), index=True)
    
    sector: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    region: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organization_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    targeted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="victims")

class CampaignTimeline(Base):
    """
    Chronological events defining the campaign lifecycle.
    """
    __tablename__ = "campaign_timeline"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("campaign_registry.id", ondelete="CASCADE"), index=True)
    
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False) # "Infrastructure Registration", "First Phish", "Data Exfil"
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="timeline_events")

class CampaignEvidence(Base):
    """
    Provenance tracking for auto-clustering.
    """
    __tablename__ = "campaign_evidence"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("campaign_registry.id", ondelete="CASCADE"), index=True)
    
    evidence_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g., "Shared IP", "Similar TTPs"
    description: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    
    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="evidence")
