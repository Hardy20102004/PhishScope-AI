from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.ai_context import ContextPolicyType

class OptimizationMetrics(BaseModel):
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    build_latency_ms: float
    cache_hit: bool

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class ContextRequest(BaseModel):
    investigation_id: Optional[str] = None
    case_id: Optional[str] = None
    query: Optional[str] = None
    template_name: Optional[str] = None
    max_tokens: int = 4096
    apply_compression: bool = True
    actor_id: str = "system"

class ContextResponse(BaseModel):
    assembled_context: str
    metrics: OptimizationMetrics
    validation: ValidationResult
    
class ContextPolicyBase(BaseModel):
    policy_type: ContextPolicyType
    name: str
    is_active: bool = True
    configuration: Optional[str] = None
    tenant_id: Optional[str] = None

class ContextPolicyResponse(ContextPolicyBase):
    id: str

    class Config:
        from_attributes = True
