import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class Incident(Base):
    __tablename__ = "ir_incidents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM") # CRITICAL, HIGH, MEDIUM, LOW
    status: Mapped[str] = mapped_column(String(50), default="NEW") # NEW, INVESTIGATING, CONTAINMENT, RESOLVED, CLOSED
    
    lead_investigator_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    cases = relationship("DFIRCase", back_populates="incident", cascade="all, delete-orphan")
    tasks = relationship("IncidentTask", back_populates="incident", cascade="all, delete-orphan")


class DFIRCase(Base):
    __tablename__ = "ir_dfir_cases"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    incident_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ir_incidents.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255))
    case_type: Mapped[str] = mapped_column(String(50)) # FORENSICS, MALWARE_ANALYSIS, CLOUD_SECURITY
    status: Mapped[str] = mapped_column(String(50), default="OPEN")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    incident = relationship("Incident", back_populates="cases")
    evidence = relationship("EvidenceRecord", back_populates="case", cascade="all, delete-orphan")


class EvidenceRecord(Base):
    __tablename__ = "ir_evidence_records"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ir_dfir_cases.id", ondelete="CASCADE"), index=True)
    
    artifact_type: Mapped[str] = mapped_column(String(50)) # FILE, HASH, IP, MEMORY_IMAGE, DISK_IMAGE
    artifact_value: Mapped[str] = mapped_column(Text) # The hash, the IP, or the file path
    source: Mapped[str] = mapped_column(String(255)) # EDR, Firewall, Memory Dump
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    case = relationship("DFIRCase", back_populates="evidence")
    chain_of_custody = relationship("ChainOfCustodyLog", back_populates="evidence", cascade="all, delete-orphan")


class ChainOfCustodyLog(Base):
    __tablename__ = "ir_chain_of_custody_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    evidence_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ir_evidence_records.id", ondelete="CASCADE"), index=True)
    
    action: Mapped[str] = mapped_column(String(100)) # COLLECTED, TRANSFERRED, ANALYZED
    performed_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    digital_signature: Mapped[str] = mapped_column(String(255)) # SHA-256 hash of the evidence state
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    evidence = relationship("EvidenceRecord", back_populates="chain_of_custody")


class IncidentTask(Base):
    __tablename__ = "ir_incident_tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    incident_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ir_incidents.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255))
    task_type: Mapped[str] = mapped_column(String(50)) # CONTAINMENT, INVESTIGATION, FORENSICS
    status: Mapped[str] = mapped_column(String(50), default="TODO") # TODO, IN_PROGRESS, REVIEW, DONE
    
    assigned_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    incident = relationship("Incident", back_populates="tasks")
