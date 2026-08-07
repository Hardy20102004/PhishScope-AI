import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base

class CriticalityLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class FindingSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class FindingType(str, enum.Enum):
    SAST = "SAST"
    DAST = "DAST"
    SCA = "SCA"
    SECRETS = "SECRETS"
    IAC = "IAC"
    CONTAINER = "CONTAINER"
    MANUAL = "MANUAL"

class FindingStatus(str, enum.Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    ACCEPTED_RISK = "ACCEPTED_RISK"
    FALSE_POSITIVE = "FALSE_POSITIVE"

class EnterpriseApplication(Base):
    """
    Core application asset identified in the enterprise.
    """
    __tablename__ = "aspm_applications"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    business_unit: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    criticality: Mapped[CriticalityLevel] = mapped_column(Enum(CriticalityLevel), default=CriticalityLevel.MEDIUM)
    is_internet_facing: Mapped[bool] = mapped_column(Boolean, default=False)
    has_pii: Mapped[bool] = mapped_column(Boolean, default=False)
    
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class CodeRepository(Base):
    """
    Source code repository tied to an application.
    """
    __tablename__ = "aspm_repositories"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_applications.id", ondelete="SET NULL"), nullable=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False) # GITHUB, GITLAB, BITBUCKET
    default_branch: Mapped[str] = mapped_column(String(100), default="main")
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_scanned: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ApplicationDependency(Base):
    """
    Software supply chain dependencies (SCA).
    """
    __tablename__ = "aspm_dependencies"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    repository_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("aspm_repositories.id", ondelete="CASCADE"))
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    ecosystem: Mapped[str] = mapped_column(String(100), nullable=False) # npm, pypi, maven
    
    is_vulnerable: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityFinding(Base):
    """
    Unified security finding from various scanners (SAST, DAST, SCA).
    """
    __tablename__ = "aspm_security_findings"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_applications.id", ondelete="CASCADE"), nullable=True)
    repository_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_repositories.id", ondelete="CASCADE"), nullable=True)
    
    finding_type: Mapped[FindingType] = mapped_column(Enum(FindingType), nullable=False)
    severity: Mapped[FindingSeverity] = mapped_column(Enum(FindingSeverity), nullable=False)
    status: Mapped[FindingStatus] = mapped_column(Enum(FindingStatus), default=FindingStatus.OPEN)
    
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(String(4000), nullable=False)
    cve_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    line_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    scanner_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class ApplicationRisk(Base):
    """
    Aggregated risk score and metrics for an application.
    """
    __tablename__ = "aspm_application_risk"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("aspm_applications.id", ondelete="CASCADE"), unique=True)
    
    overall_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    sast_score: Mapped[float] = mapped_column(Float, default=0.0)
    sca_score: Mapped[float] = mapped_column(Float, default=0.0)
    dast_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    critical_findings_count: Mapped[int] = mapped_column(Integer, default=0)
    high_findings_count: Mapped[int] = mapped_column(Integer, default=0)
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ASPMAuditLog(Base):
    """
    Audit log for changes in the ASPM platform.
    """
    __tablename__ = "aspm_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
