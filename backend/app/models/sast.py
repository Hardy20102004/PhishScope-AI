import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class ScanStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class FindingSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class SASTScan(Base):
    """
    Tracks the execution of a static analysis scan.
    """
    __tablename__ = "sast_scans"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    repository_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_repositories.id", ondelete="SET NULL"), nullable=True)
    
    branch: Mapped[str] = mapped_column(String(255), nullable=False)
    commit_sha: Mapped[str] = mapped_column(String(255), nullable=False)
    
    status: Mapped[ScanStatus] = mapped_column(Enum(ScanStatus), default=ScanStatus.QUEUED)
    
    files_scanned: Mapped[int] = mapped_column(Integer, default=0)
    lines_of_code: Mapped[int] = mapped_column(Integer, default=0)
    
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    findings: Mapped[List["SASTFinding"]] = relationship("SASTFinding", back_populates="scan", cascade="all, delete-orphan")

class SASTRule(Base):
    """
    Represents secure coding rules mapped against OWASP, CWE.
    """
    __tablename__ = "sast_rules"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    rule_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    cwe: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    owasp_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    severity: Mapped[FindingSeverity] = mapped_column(Enum(FindingSeverity), default=FindingSeverity.MEDIUM)

class SASTFinding(Base):
    """
    Represents a specific identified security weakness.
    """
    __tablename__ = "sast_findings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    scan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sast_scans.id", ondelete="CASCADE"), index=True)
    scan: Mapped["SASTScan"] = relationship("SASTScan", back_populates="findings")
    
    rule_id: Mapped[str] = mapped_column(String(100), nullable=False)
    
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)
    code_snippet: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    severity: Mapped[FindingSeverity] = mapped_column(Enum(FindingSeverity), default=FindingSeverity.MEDIUM)
    exploitability_score: Mapped[float] = mapped_column(Float, default=5.0)
    
    is_suppressed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    guidance: Mapped[Optional["SASTGuidance"]] = relationship("SASTGuidance", back_populates="finding", uselist=False, cascade="all, delete-orphan")

class SASTGuidance(Base):
    """
    Captures AI-generated remediation advice.
    """
    __tablename__ = "sast_guidance"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    finding_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sast_findings.id", ondelete="CASCADE"), unique=True)
    finding: Mapped["SASTFinding"] = relationship("SASTFinding", back_populates="guidance")
    
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    remediation_steps: Mapped[str] = mapped_column(Text, nullable=False)
    code_fix_suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SASTAuditLog(Base):
    """
    Audits scans and remediation approvals.
    """
    __tablename__ = "sast_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
