import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class SCAEcosystem(str, enum.Enum):
    NPM = "NPM"
    PYPI = "PYPI"
    MAVEN = "MAVEN"
    GRADLE = "GRADLE"
    NUGET = "NUGET"
    GO = "GO"
    RUBYGEMS = "RUBYGEMS"
    CARGO = "CARGO"
    COMPOSER = "COMPOSER"
    LINUX = "LINUX"
    UNKNOWN = "UNKNOWN"

class SCADependencyType(str, enum.Enum):
    DIRECT = "DIRECT"
    TRANSITIVE = "TRANSITIVE"

class SCARiskLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class SCAPackageIntelligence(Base):
    """
    Centralizes operational metadata for open-source components.
    """
    __tablename__ = "sca_package_intelligence"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    ecosystem: Mapped[SCAEcosystem] = mapped_column(Enum(SCAEcosystem), default=SCAEcosystem.UNKNOWN)
    package_name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    
    is_deprecated: Mapped[bool] = mapped_column(Boolean, default=False)
    is_abandoned: Mapped[bool] = mapped_column(Boolean, default=False)
    end_of_life_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    popularity_score: Mapped[float] = mapped_column(Float, default=0.0) # 0-10
    maintenance_score: Mapped[float] = mapped_column(Float, default=0.0) # 0-10
    
    known_cves: Mapped[int] = mapped_column(Integer, default=0)
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class SCADependency(Base):
    """
    Tracks a specific third-party dependency discovered within an application.
    """
    __tablename__ = "sca_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_applications.id", ondelete="CASCADE"), nullable=True)
    package_intelligence_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("sca_package_intelligence.id", ondelete="SET NULL"), nullable=True)
    
    ecosystem: Mapped[SCAEcosystem] = mapped_column(Enum(SCAEcosystem), default=SCAEcosystem.UNKNOWN)
    package_name: Mapped[str] = mapped_column(String(255), nullable=False)
    version_constraint: Mapped[str] = mapped_column(String(255), nullable=False) # e.g., ^18.0.0
    resolved_version: Mapped[str] = mapped_column(String(100), nullable=False)
    
    dependency_type: Mapped[SCADependencyType] = mapped_column(Enum(SCADependencyType), default=SCADependencyType.DIRECT)
    
    parent_dependency_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("sca_dependencies.id", ondelete="CASCADE"), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SCALicense(Base):
    """
    Captures the declared and observed open-source licenses for dependencies.
    """
    __tablename__ = "sca_licenses"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    package_intelligence_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sca_package_intelligence.id", ondelete="CASCADE"))
    
    spdx_id: Mapped[str] = mapped_column(String(100), nullable=False) # e.g., MIT, GPL-3.0
    is_copyleft: Mapped[bool] = mapped_column(Boolean, default=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=True) # Based on enterprise policy
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SCARiskScore(Base):
    """
    Quantifies the holistic risk of a component.
    """
    __tablename__ = "sca_risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    dependency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sca_dependencies.id", ondelete="CASCADE"), unique=True)
    
    vulnerability_risk: Mapped[float] = mapped_column(Float, default=0.0) # From CVEs
    license_risk: Mapped[float] = mapped_column(Float, default=0.0) # From non-compliant licenses
    operational_risk: Mapped[float] = mapped_column(Float, default=0.0) # From EOL/abandonment
    
    overall_score: Mapped[float] = mapped_column(Float, default=0.0) # 0-100
    risk_level: Mapped[SCARiskLevel] = mapped_column(Enum(SCARiskLevel), default=SCARiskLevel.INFO)
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SCAGuidance(Base):
    """
    Captures AI-generated upgrade paths and remediation advice.
    """
    __tablename__ = "sca_guidance"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    dependency_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sca_dependencies.id", ondelete="CASCADE"), unique=True)
    
    recommended_version: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    upgrade_complexity: Mapped[str] = mapped_column(String(50), default="LOW") # LOW, MEDIUM, HIGH
    remediation_steps: Mapped[str] = mapped_column(Text, nullable=False)
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SCAAuditLog(Base):
    """
    Audit log for software composition analysis.
    """
    __tablename__ = "sca_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
