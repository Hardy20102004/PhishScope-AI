import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

class DetectionRuleVersionBase(BaseModel):
    version: int
    payload: str
    change_summary: Optional[str] = None

class DetectionRuleVersionCreate(DetectionRuleVersionBase):
    pass

class DetectionRuleVersionResponse(DetectionRuleVersionBase):
    id: uuid.UUID
    rule_id: uuid.UUID
    author_id: Optional[uuid.UUID]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DetectionRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    rule_type: str = Field(..., description="SIGMA, YARA, CUSTOM")
    severity: str = Field(default="MEDIUM")
    mitre_tactics: Optional[Dict[str, Any]] = None
    mitre_techniques: Optional[Dict[str, Any]] = None
    tags: Optional[Dict[str, Any]] = None

class DetectionRuleCreate(DetectionRuleBase):
    payload: str = Field(..., description="The raw rule content (YAML, JSON, YARA)")

class DetectionRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    mitre_tactics: Optional[Dict[str, Any]] = None
    mitre_techniques: Optional[Dict[str, Any]] = None
    tags: Optional[Dict[str, Any]] = None
    
    new_payload: Optional[str] = Field(None, description="Provide this to create a new version of the rule")
    change_summary: Optional[str] = None

class DetectionRuleResponse(DetectionRuleBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    author_id: Optional[uuid.UUID]
    owner_id: Optional[uuid.UUID]
    status: str
    current_version: int
    created_at: datetime
    updated_at: datetime
    
    # versions: List[DetectionRuleVersionResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class RuleTestResultBase(BaseModel):
    dataset_name: str
    coverage_score: float
    false_positives: int
    false_negatives: int
    execution_time_ms: int
    passed: bool

class RuleTestResultResponse(RuleTestResultBase):
    id: uuid.UUID
    rule_id: uuid.UUID
    version_id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class RuleApprovalRecordCreate(BaseModel):
    status_changed_to: str = Field(..., description="APPROVED, READY_FOR_DEPLOYMENT, etc")
    notes: Optional[str] = None

class RuleApprovalRecordResponse(BaseModel):
    id: uuid.UUID
    rule_id: uuid.UUID
    version_id: uuid.UUID
    approver_id: uuid.UUID
    status_changed_to: str
    notes: Optional[str]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
