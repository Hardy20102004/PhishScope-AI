import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class HuntSession(Base):
    __tablename__ = "threat_hunt_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255), index=True)
    objective: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", index=True) # ACTIVE, COMPLETED, ARCHIVED
    
    assigned_hunter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    queries = relationship("HuntQuery", back_populates="session", cascade="all, delete-orphan")
    hypotheses = relationship("HuntHypothesis", back_populates="session", cascade="all, delete-orphan")
    evidence = relationship("HuntEvidence", back_populates="session", cascade="all, delete-orphan")


class HuntQuery(Base):
    __tablename__ = "threat_hunt_queries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("threat_hunt_sessions.id", ondelete="CASCADE"), index=True)
    
    query_type: Mapped[str] = mapped_column(String(50), default="NATURAL_LANGUAGE") # NATURAL_LANGUAGE, STRUCTURED
    raw_query: Mapped[str] = mapped_column(Text)
    translated_structured_query: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    results_count: Mapped[int] = mapped_column(Integer, default=0)
    execution_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("HuntSession", back_populates="queries")


class HuntHypothesis(Base):
    __tablename__ = "threat_hunt_hypotheses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("threat_hunt_sessions.id", ondelete="CASCADE"), index=True)
    
    hypothesis_text: Mapped[str] = mapped_column(Text)
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    mitre_tactics: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    mitre_techniques: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    suggested_queries: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    status: Mapped[str] = mapped_column(String(50), default="PROPOSED") # PROPOSED, PROVEN, DISPROVEN
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("HuntSession", back_populates="hypotheses")


class HuntEvidence(Base):
    __tablename__ = "threat_hunt_evidence"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("threat_hunt_sessions.id", ondelete="CASCADE"), index=True)
    
    evidence_type: Mapped[str] = mapped_column(String(50)) # ALERT, IOC, GRAPH_NODE, EVENT
    reference_id: Mapped[str] = mapped_column(String(255)) # ID of the related object
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_key_finding: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("HuntSession", back_populates="evidence")
