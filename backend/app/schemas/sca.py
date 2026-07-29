from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.sca import SCAEcosystem, SCADependencyType, SCARiskLevel

# --- Package Intelligence ---
class SCAPackageIntelligenceBase(BaseModel):
    ecosystem: SCAEcosystem
    package_name: str
    version: str
    is_deprecated: bool = False
    is_abandoned: bool = False
    end_of_life_date: Optional[datetime] = None
    popularity_score: float = 0.0
    maintenance_score: float = 0.0
    known_cves: int = 0

class SCAPackageIntelligenceCreate(SCAPackageIntelligenceBase):
    pass

class SCAPackageIntelligenceResponse(SCAPackageIntelligenceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Dependency ---
class SCADependencyBase(BaseModel):
    ecosystem: SCAEcosystem
    package_name: str
    version_constraint: str
    resolved_version: str
    dependency_type: SCADependencyType = SCADependencyType.DIRECT

class SCADependencyCreate(SCADependencyBase):
    application_id: Optional[uuid.UUID] = None
    package_intelligence_id: Optional[uuid.UUID] = None
    parent_dependency_id: Optional[uuid.UUID] = None

class SCADependencyResponse(SCADependencyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    application_id: Optional[uuid.UUID]
    package_intelligence_id: Optional[uuid.UUID]
    parent_dependency_id: Optional[uuid.UUID]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- License ---
class SCALicenseBase(BaseModel):
    spdx_id: str
    is_copyleft: bool = False
    is_approved: bool = True

class SCALicenseCreate(SCALicenseBase):
    package_intelligence_id: uuid.UUID

class SCALicenseResponse(SCALicenseBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    package_intelligence_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Risk Score ---
class SCARiskScoreBase(BaseModel):
    vulnerability_risk: float = 0.0
    license_risk: float = 0.0
    operational_risk: float = 0.0
    overall_score: float = 0.0
    risk_level: SCARiskLevel = SCARiskLevel.INFO

class SCARiskScoreCreate(SCARiskScoreBase):
    dependency_id: uuid.UUID

class SCARiskScoreResponse(SCARiskScoreBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    dependency_id: uuid.UUID
    calculated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Guidance ---
class SCAGuidanceBase(BaseModel):
    recommended_version: Optional[str] = None
    upgrade_complexity: str = "LOW"
    remediation_steps: str

class SCAGuidanceCreate(SCAGuidanceBase):
    dependency_id: uuid.UUID

class SCAGuidanceResponse(SCAGuidanceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    dependency_id: uuid.UUID
    generated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Executive Summary ---
class SCAExecutiveSummary(BaseModel):
    total_dependencies: int
    vulnerable_dependencies: int
    license_violations: int
    average_risk_score: float
    abandoned_packages: int
