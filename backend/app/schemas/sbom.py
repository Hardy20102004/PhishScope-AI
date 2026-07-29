from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.sbom import SBOMFormat, IntegrityStatus

# --- SBOM Record ---
class SBOMRecordBase(BaseModel):
    name: str
    version: str
    format: SBOMFormat = SBOMFormat.CYCLONEDX
    component_count: int = 0
    raw_data: Optional[Dict[str, Any]] = None

class SBOMRecordCreate(SBOMRecordBase):
    application_id: Optional[uuid.UUID] = None

class SBOMRecordResponse(SBOMRecordBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    application_id: Optional[uuid.UUID]
    ingested_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Software Artifact ---
class SoftwareArtifactBase(BaseModel):
    name: str
    type: str
    version: str
    purl: Optional[str] = None
    hash_sha256: Optional[str] = None

class SoftwareArtifactCreate(SoftwareArtifactBase):
    sbom_id: Optional[uuid.UUID] = None

class SoftwareArtifactResponse(SoftwareArtifactBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    sbom_id: Optional[uuid.UUID]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Software Dependency ---
class SoftwareDependencyBase(BaseModel):
    name: str
    version: str
    purl: Optional[str] = None
    is_direct: bool = True
    license: Optional[str] = None
    is_end_of_life: bool = False

class SoftwareDependencyCreate(SoftwareDependencyBase):
    sbom_id: uuid.UUID

class SoftwareDependencyResponse(SoftwareDependencyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    sbom_id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

# --- Provenance Metadata ---
class ProvenanceMetadataBase(BaseModel):
    builder_id: str
    build_type: str
    slsa_level: int = 0
    integrity_status: IntegrityStatus = IntegrityStatus.UNVERIFIED

class ProvenanceMetadataCreate(ProvenanceMetadataBase):
    artifact_id: uuid.UUID

class ProvenanceMetadataResponse(ProvenanceMetadataBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    artifact_id: uuid.UUID
    verified_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# --- Supply Chain Risk Score ---
class SupplyChainRiskScoreBase(BaseModel):
    overall_score: float = 100.0
    vulnerability_risk: float = 0.0
    license_risk: float = 0.0
    provenance_risk: float = 0.0

class SupplyChainRiskScoreCreate(SupplyChainRiskScoreBase):
    sbom_id: uuid.UUID

class SupplyChainRiskScoreResponse(SupplyChainRiskScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    sbom_id: uuid.UUID
    calculated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- SBOM Executive Summary ---
class SBOMExecutiveSummary(BaseModel):
    total_sboms: int
    total_artifacts: int
    total_dependencies: int
    unverified_provenance: int
    average_supply_chain_score: float
