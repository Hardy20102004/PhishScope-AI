import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class UnifiedInvestigation(Base):
    __tablename__ = "mf_unified_investigations"
    """
    Root entity managing a timeline correlation session.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=True)
    
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    events = relationship("UnifiedTimelineEvent", back_populates="investigation", cascade="all, delete-orphan")
    correlations = relationship("EvidenceCorrelation", back_populates="investigation", cascade="all, delete-orphan")


class UnifiedTimelineEvent(Base):
    __tablename__ = "mf_unified_events"
    """
    Normalized wrapper representing a single point in time across any forensic module.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    inv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_unified_investigations.id", ondelete="CASCADE"), index=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    
    # Polymorphic references
    source_module: Mapped[str] = mapped_column(String(50), index=True) # DISK, MEMORY, CLOUD, EMAIL
    source_table: Mapped[str] = mapped_column(String(100)) # e.g. mf_cloud_audit_logs
    source_id: Mapped[str] = mapped_column(String(100)) # e.g. uuid of the audit log
    
    event_type: Mapped[str] = mapped_column(String(100)) # e.g. IAM_ASSUME_ROLE, FILE_EXECUTION
    event_summary: Mapped[str] = mapped_column(Text)
    
    # JSON payload for immediate rendering without joining back to source
    render_metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    investigation = relationship("UnifiedInvestigation", back_populates="events")


class EvidenceCorrelation(Base):
    __tablename__ = "mf_evidence_correlations"
    """
    Explicit links between events sharing the same IOCs.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    inv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_unified_investigations.id", ondelete="CASCADE"), index=True)
    
    event_a_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_unified_events.id", ondelete="CASCADE"))
    event_b_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_unified_events.id", ondelete="CASCADE"))
    
    correlation_type: Mapped[str] = mapped_column(String(50)) # SHARED_IP, SHARED_HASH, CAUSAL
    correlation_value: Mapped[str] = mapped_column(String(255)) # e.g. 203.0.113.5
    confidence_score: Mapped[int] = mapped_column(Integer, default=100)
    
    investigation = relationship("UnifiedInvestigation", back_populates="correlations")

    # Relationships to the specific events could be added here if needed, 
    # but often explicit queries are used for graph generation.
