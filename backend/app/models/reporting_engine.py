import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class EvidenceItem(Base):
    __tablename__ = "mf_evidence_items"
    """
    Tracks the ingestion of raw forensic artifacts.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=True)
    
    name: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(100)) # DISK_IMAGE, CLOUDTRAIL_JSON, MEMORY_DUMP
    
    original_sha256: Mapped[str] = mapped_column(String(64), index=True)
    acquisition_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    acquired_by: Mapped[str] = mapped_column(String(255)) # User ID / Name
    
    chain_of_custody = relationship("ChainOfCustodyRecord", back_populates="evidence", cascade="all, delete-orphan")


class ChainOfCustodyRecord(Base):
    __tablename__ = "mf_chain_of_custody"
    """
    Immutable ledger of evidence handling.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    evidence_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_evidence_items.id", ondelete="CASCADE"), index=True)
    
    action_type: Mapped[str] = mapped_column(String(50)) # INGEST, TRANSFER, ANALYSIS, ARCHIVE
    actor_id: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Cryptographic validation that this record hasn't been altered
    record_hash: Mapped[str] = mapped_column(String(64)) 
    
    evidence = relationship("EvidenceItem", back_populates="chain_of_custody")


class ForensicReport(Base):
    __tablename__ = "mf_forensic_reports"
    """
    Generated output document.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=True)
    
    title: Mapped[str] = mapped_column(String(255))
    report_type: Mapped[str] = mapped_column(String(50)) # COURT_READY, EXECUTIVE, TECHNICAL
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    author_id: Mapped[str] = mapped_column(String(255))
    
    is_finalized: Mapped[bool] = mapped_column(Boolean, default=False)
    digital_signature: Mapped[str] = mapped_column(String(512), nullable=True) # Validates the final document
    
    sections = relationship("ReportSection", back_populates="report", cascade="all, delete-orphan")


class ReportSection(Base):
    __tablename__ = "mf_report_sections"
    """
    Hierarchical blocks of a report.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_forensic_reports.id", ondelete="CASCADE"), index=True)
    
    section_type: Mapped[str] = mapped_column(String(100)) # e.g. EXECUTIVE_SUMMARY, TIMELINE_CORRELATION
    order_index: Mapped[int] = mapped_column(Integer)
    
    content: Mapped[str] = mapped_column(Text)
    
    # Explicit traceability links to underlying evidence IDs
    linked_evidence_ids: Mapped[dict] = mapped_column(JSON, default=list) 
    
    report = relationship("ForensicReport", back_populates="sections")
