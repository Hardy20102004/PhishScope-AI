import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class TimelineType(str, enum.Enum):
    INVESTIGATION = "INVESTIGATION"
    CAMPAIGN = "CAMPAIGN"
    THREAT_ACTOR = "THREAT_ACTOR"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    IOC = "IOC"
    MALWARE = "MALWARE"
    VICTIM = "VICTIM"
    UNIFIED = "UNIFIED"

class EventCategory(str, enum.Enum):
    OBSERVATION = "OBSERVATION"
    CREATION = "CREATION"
    MODIFICATION = "MODIFICATION"
    DELETION = "DELETION"
    EXECUTION = "EXECUTION"
    COMMUNICATION = "COMMUNICATION"
    ANALYST_FINDING = "ANALYST_FINDING"

class Timeline(Base):
    __tablename__ = "timelines"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    timeline_type = Column(Enum(TimelineType), nullable=False)
    tenant_id = Column(String, nullable=True, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    events = relationship("ThreatTimelineEvent", back_populates="timeline", cascade="all, delete-orphan")


class ThreatTimelineEvent(Base):
    __tablename__ = "threat_timeline_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timeline_id = Column(String, ForeignKey("timelines.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Core Chronology
    timestamp = Column(DateTime, nullable=False, index=True) # Normalized to UTC
    
    # Event Details
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(Enum(EventCategory), default=EventCategory.OBSERVATION)
    
    # Relationships & Ontology mappings
    entity_id = Column(String, nullable=True, index=True) # Ref to knowledge graph entity if applicable
    
    # Explainability
    confidence = Column(Float, default=1.0)
    is_hypothetical = Column(Boolean, default=False) # For Historical Reconstruction Engine
    
    # Extensibility
    properties_json = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    timeline = relationship("Timeline", back_populates="events")
    evidence = relationship("EventEvidence", back_populates="event", cascade="all, delete-orphan")


class EventEvidence(Base):
    __tablename__ = "timeline_event_evidence"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String, ForeignKey("threat_timeline_events.id", ondelete="CASCADE"), nullable=False, index=True)
    
    source_type = Column(String, nullable=False) # e.g. PCAP, REPORT, AI_MEMORY, FEED
    reference_url = Column(String, nullable=True)
    snippet = Column(String, nullable=True)
    
    event = relationship("ThreatTimelineEvent", back_populates="evidence")
