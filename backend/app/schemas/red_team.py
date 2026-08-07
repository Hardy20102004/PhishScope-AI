import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

class AuthorizationRecordBase(BaseModel):
    stakeholder_role: str
    stakeholder_id: str
    is_approved: bool
    signature_hash: Optional[str]
    approved_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class CampaignFindingBase(BaseModel):
    title: str
    description: str
    severity: str
    tactic: Optional[str]
    technique_id: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class RedTeamCampaignBase(BaseModel):
    name: str
    description: str
    scope_definition: Dict[str, Any]

class RedTeamCampaignResponse(RedTeamCampaignBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    
    approvals: List[AuthorizationRecordBase] = []
    findings: List[CampaignFindingBase] = []
    
    model_config = ConfigDict(from_attributes=True)
