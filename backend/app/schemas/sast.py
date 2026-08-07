from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
import uuid

from app.models.sast import ScanStatus, FindingSeverity

# --- SAST Rule ---
class SASTRuleBase(BaseModel):
    rule_id: str
    name: str
    description: str
    cwe: Optional[str] = None
    owasp_category: Optional[str] = None
    severity: FindingSeverity = FindingSeverity.MEDIUM

class SASTRuleCreate(SASTRuleBase):
    pass

class SASTRuleResponse(SASTRuleBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

# --- SAST Guidance ---
class SASTGuidanceBase(BaseModel):
    explanation: str
    remediation_steps: str
    code_fix_suggestion: Optional[str] = None

class SASTGuidanceCreate(SASTGuidanceBase):
    finding_id: uuid.UUID

class SASTGuidanceResponse(SASTGuidanceBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    finding_id: uuid.UUID
    generated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- SAST Finding ---
class SASTFindingBase(BaseModel):
    rule_id: str
    file_path: str
    line_number: int
    code_snippet: Optional[str] = None
    severity: FindingSeverity = FindingSeverity.MEDIUM
    exploitability_score: float = 5.0
    is_suppressed: bool = False

class SASTFindingCreate(SASTFindingBase):
    scan_id: uuid.UUID

class SASTFindingResponse(SASTFindingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    scan_id: uuid.UUID
    created_at: datetime
    guidance: Optional[SASTGuidanceResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

# --- SAST Scan ---
class SASTScanBase(BaseModel):
    branch: str
    commit_sha: str
    status: ScanStatus = ScanStatus.QUEUED
    files_scanned: int = 0
    lines_of_code: int = 0

class SASTScanCreate(SASTScanBase):
    repository_id: Optional[uuid.UUID] = None

class SASTScanResponse(SASTScanBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    repository_id: Optional[uuid.UUID]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    findings: List[SASTFindingResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# --- SAST Executive Summary ---
class SASTExecutiveSummary(BaseModel):
    total_scans: int
    critical_findings: int
    high_findings: int
    average_lines_scanned: int
