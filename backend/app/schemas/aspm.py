from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.aspm import CriticalityLevel, FindingSeverity, FindingType, FindingStatus

# --- Applications ---
class EnterpriseApplicationBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner: Optional[str] = None
    business_unit: Optional[str] = None
    criticality: CriticalityLevel = CriticalityLevel.MEDIUM
    is_internet_facing: bool = False
    has_pii: bool = False
    metadata_json: Dict[str, Any] = {}

class EnterpriseApplicationCreate(EnterpriseApplicationBase):
    pass

class EnterpriseApplicationResponse(EnterpriseApplicationBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Repositories ---
class CodeRepositoryBase(BaseModel):
    name: str
    url: str
    provider: str
    default_branch: str = "main"
    is_active: bool = True

class CodeRepositoryCreate(CodeRepositoryBase):
    application_id: Optional[uuid.UUID] = None

class CodeRepositoryResponse(CodeRepositoryBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    application_id: Optional[uuid.UUID]
    last_scanned: Optional[datetime]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Dependencies ---
class ApplicationDependencyBase(BaseModel):
    name: str
    version: str
    ecosystem: str
    is_vulnerable: bool = False

class ApplicationDependencyCreate(ApplicationDependencyBase):
    repository_id: uuid.UUID

class ApplicationDependencyResponse(ApplicationDependencyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    repository_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Security Findings ---
class SecurityFindingBase(BaseModel):
    finding_type: FindingType
    severity: FindingSeverity
    status: FindingStatus = FindingStatus.OPEN
    title: str
    description: str
    cve_id: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    scanner_name: str

class SecurityFindingCreate(SecurityFindingBase):
    application_id: Optional[uuid.UUID] = None
    repository_id: Optional[uuid.UUID] = None

class SecurityFindingResponse(SecurityFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    application_id: Optional[uuid.UUID]
    repository_id: Optional[uuid.UUID]
    created_at: datetime
    resolved_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

# --- Risk ---
class ApplicationRiskResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    application_id: uuid.UUID
    overall_risk_score: float
    sast_score: float
    sca_score: float
    dast_score: float
    critical_findings_count: int
    high_findings_count: int
    calculated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ASPMExecutiveSummary(BaseModel):
    total_applications: int
    critical_applications: int
    total_repositories: int
    average_risk_score: float
    open_critical_findings: int
    open_high_findings: int
