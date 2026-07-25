from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.decision import DecisionState, DecisionType

# Sub-components for reasoning JSON

class ReasoningStep(BaseModel):
    step: int
    observation: str
    inference: str

class AlternativeHypothesis(BaseModel):
    hypothesis: str
    probability: float
    missing_evidence: List[str]

class RecommendationItem(BaseModel):
    action: str
    priority: str # HIGH, MEDIUM, LOW
    description: str

class EvidenceLinkBase(BaseModel):
    source_type: str
    source_id: str
    description: Optional[str] = None

class EvidenceLinkResponse(EvidenceLinkBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)

class ApprovalWorkflowResponse(BaseModel):
    id: str
    user_id: str
    action: str
    comments: Optional[str]
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Core Decision Schemas

class DecisionBase(BaseModel):
    decision_type: DecisionType
    case_id: Optional[str] = None
    summary: str
    confidence: float
    
    reasoning_chain: List[ReasoningStep] = []
    assumptions: List[str] = []
    limitations: List[str] = []
    alternatives: List[AlternativeHypothesis] = []
    recommendations: List[RecommendationItem] = []

class DecisionCreate(DecisionBase):
    evidence: List[EvidenceLinkBase] = []

class DecisionResponse(DecisionBase):
    id: str
    tenant_id: Optional[str] = None
    state: DecisionState
    created_at: datetime
    updated_at: datetime
    
    evidence_links: List[EvidenceLinkResponse] = []
    workflow_logs: List[ApprovalWorkflowResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class HumanReviewRequest(BaseModel):
    action: str # "APPROVE", "REJECT"
    comments: str
