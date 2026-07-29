from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.dast import DASTScanStatus, DASTFindingSeverity, DASTTargetType

# --- DAST Target ---
class DASTTargetBase(BaseModel):
    name: str
    base_url: str
    target_type: DASTTargetType = DASTTargetType.WEB_APP
    auth_method: Optional[str] = None

class DASTTargetCreate(DASTTargetBase):
    application_id: Optional[uuid.UUID] = None

class DASTTargetResponse(DASTTargetBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    application_id: Optional[uuid.UUID]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- DAST Scan ---
class DASTScanBase(BaseModel):
    status: DASTScanStatus = DASTScanStatus.QUEUED
    endpoints_tested: int = 0

class DASTScanCreate(DASTScanBase):
    target_id: uuid.UUID

class DASTScanResponse(DASTScanBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    target_id: uuid.UUID
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# --- DAST Finding ---
class DASTFindingBase(BaseModel):
    vulnerability_name: str
    cwe: Optional[str] = None
    url: str
    method: str
    request_payload: Optional[str] = None
    response_snippet: Optional[str] = None
    severity: DASTFindingSeverity = DASTFindingSeverity.MEDIUM
    exploitability_score: float = 5.0
    is_suppressed: bool = False

class DASTFindingCreate(DASTFindingBase):
    scan_id: uuid.UUID

class DASTFindingResponse(DASTFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    scan_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- DAST Guidance ---
class DASTGuidanceBase(BaseModel):
    explanation: str
    remediation_steps: str
    configuration_fix: Optional[str] = None

class DASTGuidanceCreate(DASTGuidanceBase):
    finding_id: uuid.UUID

class DASTGuidanceResponse(DASTGuidanceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    finding_id: uuid.UUID
    generated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- DAST Executive Summary ---
class DASTExecutiveSummary(BaseModel):
    total_targets: int
    active_scans: int
    critical_findings: int
    high_findings: int
    endpoints_assessed_30d: int
