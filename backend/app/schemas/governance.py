import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional

class SecurityPolicyBase(BaseModel):
    policy_name: str
    policy_domain: str
    description: str
    rule_logic: Dict[str, Any]
    is_active: bool

class SecurityPolicyResponse(SecurityPolicyBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    version: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class GovernanceWorkflowBase(BaseModel):
    workflow_name: str
    workflow_type: str
    status: str
    context_data: Dict[str, Any]

class GovernanceWorkflowResponse(GovernanceWorkflowBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ApprovalRecordBase(BaseModel):
    workflow_id: uuid.UUID
    approver_id: str
    approver_role: str
    action: str
    comments: Optional[str] = None

class ApprovalRecordResponse(ApprovalRecordBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    signed_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AutomationLogBase(BaseModel):
    workflow_id: uuid.UUID
    task_name: str
    status: str
    execution_details: Dict[str, Any]

class AutomationLogResponse(AutomationLogBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    executed_at: datetime
    model_config = ConfigDict(from_attributes=True)
