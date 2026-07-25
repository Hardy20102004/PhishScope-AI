from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# AI Provider Schemas
class AIProviderBase(BaseModel):
    name: str
    base_url: Optional[str] = None
    api_key_secret: Optional[str] = None
    is_active: bool = True

class AIProviderCreate(AIProviderBase):
    pass

class AIProviderResponse(AIProviderBase):
    id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# AI Model Schemas
class AIModelBase(BaseModel):
    name: str
    version: Optional[str] = None
    provider_id: str
    capabilities: List[str] = []
    context_window: int = 8192
    cost_per_1k_prompt: float = 0.0
    cost_per_1k_completion: float = 0.0
    is_active: bool = True

class AIModelCreate(AIModelBase):
    pass

class AIModelResponse(AIModelBase):
    id: str
    health_status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Routing Policy Schemas
class RoutingPolicyBase(BaseModel):
    capability: str
    primary_model_id: Optional[str] = None
    fallback_model_id: Optional[str] = None
    max_cost_limit: Optional[float] = None
    is_active: bool = True

class RoutingPolicyCreate(RoutingPolicyBase):
    pass

class RoutingPolicyResponse(RoutingPolicyBase):
    id: str
    created_at: datetime
    primary_model: Optional[AIModelResponse] = None
    fallback_model: Optional[AIModelResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

# Cost Log Schemas
class ModelCostLogBase(BaseModel):
    tenant_id: Optional[str] = None
    model_id: str
    task_type: str
    prompt_tokens: int
    completion_tokens: int
    total_cost: float

class ModelCostLogResponse(ModelCostLogBase):
    id: str
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class RoutingRequest(BaseModel):
    capability: str
    tenant_id: Optional[str] = None
    
class RoutingResponse(BaseModel):
    model: AIModelResponse
    is_fallback: bool
