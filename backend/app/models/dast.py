import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class DASTTargetType(str, enum.Enum):
    WEB_APP = "WEB_APP"
    REST_API = "REST_API"
    GRAPHQL_API = "GRAPHQL_API"
    SOAP_SERVICE = "SOAP_SERVICE"

class DASTScanStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class DASTFindingSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class DASTTarget(Base):
    """
    Web application or API being assessed.
    """
    __tablename__ = "dast_targets"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_applications.id", ondelete="SET NULL"), nullable=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    base_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    target_type: Mapped[DASTTargetType] = mapped_column(Enum(DASTTargetType), default=DASTTargetType.WEB_APP)
    
    auth_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # e.g., OIDC, API_KEY, BASIC
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DASTScan(Base):
    """
    Tracks dynamic scan executions.
    """
    __tablename__ = "dast_scans"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    target_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dast_targets.id", ondelete="CASCADE"), index=True)
    target: Mapped["DASTTarget"] = relationship("DASTTarget")
    
    status: Mapped[DASTScanStatus] = mapped_column(Enum(DASTScanStatus), default=DASTScanStatus.QUEUED)
    
    endpoints_tested: Mapped[int] = mapped_column(Integer, default=0)
    
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class DASTFinding(Base):
    """
    Security weaknesses found at runtime.
    """
    __tablename__ = "dast_findings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    scan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dast_scans.id", ondelete="CASCADE"), index=True)
    
    vulnerability_name: Mapped[str] = mapped_column(String(255), nullable=False)
    cwe: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    method: Mapped[str] = mapped_column(String(20), nullable=False) # GET, POST
    
    request_payload: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    response_snippet: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    severity: Mapped[DASTFindingSeverity] = mapped_column(Enum(DASTFindingSeverity), default=DASTFindingSeverity.MEDIUM)
    exploitability_score: Mapped[float] = mapped_column(Float, default=5.0)
    
    is_suppressed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DASTGuidance(Base):
    """
    Captures AI-generated remediation advice for DAST findings.
    """
    __tablename__ = "dast_guidance"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    finding_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dast_findings.id", ondelete="CASCADE"), unique=True)
    
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    remediation_steps: Mapped[str] = mapped_column(Text, nullable=False)
    configuration_fix: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class DASTAuditLog(Base):
    """
    Audit log for dynamic assessments.
    """
    __tablename__ = "dast_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
