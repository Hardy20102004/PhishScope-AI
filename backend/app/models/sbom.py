import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class SBOMFormat(str, enum.Enum):
    CYCLONEDX = "CYCLONEDX"
    SPDX = "SPDX"
    CUSTOM = "CUSTOM"

class IntegrityStatus(str, enum.Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    TAMPERED = "TAMPERED"

class SBOMRecord(Base):
    """
    Tracks ingested SBOM documents.
    """
    __tablename__ = "sbom_records"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("aspm_applications.id", ondelete="SET NULL"), nullable=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    format: Mapped[SBOMFormat] = mapped_column(Enum(SBOMFormat), default=SBOMFormat.CYCLONEDX)
    
    component_count: Mapped[int] = mapped_column(Integer, default=0)
    
    raw_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True) # Full SBOM JSON
    
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SoftwareArtifact(Base):
    """
    Tracks binary artifacts, container images, packages.
    """
    __tablename__ = "sbom_software_artifacts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    sbom_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("sbom_records.id", ondelete="SET NULL"), nullable=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. CONTAINER_IMAGE, NPM_PACKAGE, JAR
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    
    purl: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # Package URL
    hash_sha256: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SoftwareDependency(Base):
    """
    Represents direct and transitive dependencies.
    """
    __tablename__ = "sbom_software_dependencies"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    sbom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sbom_records.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    purl: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    is_direct: Mapped[bool] = mapped_column(Boolean, default=True)
    license: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    is_end_of_life: Mapped[bool] = mapped_column(Boolean, default=False)

class ProvenanceMetadata(Base):
    """
    Captures SLSA and in-toto provenance metadata.
    """
    __tablename__ = "sbom_provenance_metadata"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    artifact_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sbom_software_artifacts.id", ondelete="CASCADE"), index=True)
    
    builder_id: Mapped[str] = mapped_column(String(255), nullable=False)
    build_type: Mapped[str] = mapped_column(String(255), nullable=False)
    
    slsa_level: Mapped[int] = mapped_column(Integer, default=0)
    
    integrity_status: Mapped[IntegrityStatus] = mapped_column(Enum(IntegrityStatus), default=IntegrityStatus.UNVERIFIED)
    
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class SupplyChainRiskScore(Base):
    """
    Computes overall risk metrics.
    """
    __tablename__ = "sbom_supply_chain_risks"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    sbom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sbom_records.id", ondelete="CASCADE"), index=True)
    
    overall_score: Mapped[float] = mapped_column(Float, default=100.0) # 0-100 (100 = critical risk, or maybe 100 = secure. Let's say 100 = fully secure)
    
    vulnerability_risk: Mapped[float] = mapped_column(Float, default=0.0)
    license_risk: Mapped[float] = mapped_column(Float, default=0.0)
    provenance_risk: Mapped[float] = mapped_column(Float, default=0.0)
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SBOMAuditLog(Base):
    """
    Audit log for SBOM actions.
    """
    __tablename__ = "sbom_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
