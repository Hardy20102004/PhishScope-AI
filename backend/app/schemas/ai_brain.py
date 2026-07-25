from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict
import uuid
from app.models.ai_brain import ProviderType, ModelHealthStatus, MemoryTier

# ----------------- Orchestration & Response Schemas -----------------
class OrchestrationRequest(BaseModel):
    intent: Optional[str] = Field(default="GENERAL_QUERY", description="Detected or explicitly specified user intent")
    capability: Optional[str] = Field(default="Threat Analysis", description="Required AI capability (e.g. Summarization, Threat Analysis, Reasoning)")
    input_text: str = Field(..., description="Primary prompt or evidence query text")
    case_id: Optional[uuid.UUID] = Field(default=None, description="Associated Case UUID if within an investigation")
    investigation_id: Optional[uuid.UUID] = Field(default=None, description="Associated Investigation UUID")
    session_id: Optional[str] = Field(default=None, description="Session string for conversational multi-turn correlation")
    tenant_id: Optional[uuid.UUID] = Field(default=None, description="Tenant ID for policy enforcement and token consumption")
    user_id: Optional[uuid.UUID] = Field(default=None, description="Executing security analyst User UUID")
    additional_context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Supplementary context indicators, logs, or notes")
    override_model_id: Optional[str] = Field(default=None, description="Optional override to execute against a specific model ID")

class DecisionTraceStep(BaseModel):
    step_number: int
    step_name: str
    rationale: str
    confidence: float
    output: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OrchestrationResponse(BaseModel):
    request_id: str = Field(..., description="Unique immutable request tracing ID")
    response_text: str = Field(..., description="Final synthesized and validated AI response")
    provider_used: str = Field(..., description="Actual LLM provider that successfully executed the prompt")
    model_used: str = Field(..., description="Actual model identifier utilized")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Synthesized confidence calculation across evidence and reasoning")
    evidence_references: List[Dict[str, Any]] = Field(default_factory=list, description="Verified citations to real workspace IOCs or evidence URLs")
    hallucination_indicators_detected: List[str] = Field(default_factory=list, description="Flagged potential hallucination terms or unsupported claims")
    decision_trace: List[DecisionTraceStep] = Field(default_factory=list, description="Step-by-step reasoning and failover decision logs")
    token_usage: Dict[str, Union[int, float]] = Field(default_factory=dict, description="Input/output token counts and calculated cost in USD")
    latency_ms: int = Field(default=0, description="Total end-to-end execution latency in milliseconds")
    policy_status: str = Field(default="PASSED", description="Policy compliance check status (PASSED, MODIFIED, BLOCKED)")

    model_config = ConfigDict(from_attributes=True)

# ----------------- Provider & Model Registries -----------------
class AIProviderConfigBase(BaseModel):
    name: str
    provider_type: ProviderType
    base_url: Optional[str] = None
    is_active: bool = True
    priority: int = 100
    timeout_seconds: int = 30
    max_retries: int = 3

class AIProviderConfigCreate(AIProviderConfigBase):
    api_key: Optional[str] = None # Will be encrypted before storage

class AIProviderConfigUpdate(BaseModel):
    name: Optional[str] = None
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    timeout_seconds: Optional[int] = None
    max_retries: Optional[int] = None

class AIProviderConfigResponse(AIProviderConfigBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AIModelEntryBase(BaseModel):
    provider_id: uuid.UUID
    model_id: str
    display_name: str
    version: Optional[str] = None
    max_context_tokens: int = 128000
    max_output_tokens: int = 4096
    supported_languages: List[str] = ["en", "es", "fr", "de", "zh", "ja"]
    cost_per_1k_input_usd: float = 0.003
    cost_per_1k_output_usd: float = 0.015
    typical_latency_ms: int = 800
    is_available: bool = True
    health_status: ModelHealthStatus = ModelHealthStatus.HEALTHY
    capabilities_json: List[str] = []

class AIModelEntryCreate(AIModelEntryBase):
    pass

class AIModelEntryUpdate(BaseModel):
    display_name: Optional[str] = None
    version: Optional[str] = None
    max_context_tokens: Optional[int] = None
    max_output_tokens: Optional[int] = None
    cost_per_1k_input_usd: Optional[float] = None
    cost_per_1k_output_usd: Optional[float] = None
    typical_latency_ms: Optional[int] = None
    is_available: Optional[bool] = None
    health_status: Optional[ModelHealthStatus] = None
    capabilities_json: Optional[List[str]] = None

class AIModelEntryResponse(AIModelEntryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------- Capability & Prompt Registries -----------------
class AICapabilityMappingBase(BaseModel):
    capability_name: str
    description: Optional[str] = None
    default_model_id: str
    fallback_model_ids_json: List[str] = []
    parameters_json: Dict[str, Any] = {"temperature": 0.2, "top_p": 0.95}

class AICapabilityMappingCreate(AICapabilityMappingBase):
    pass

class AICapabilityMappingResponse(AICapabilityMappingBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AIPromptTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    template_type: str
    system_prompt: str
    user_template: str
    version: str = "1.0.0"
    is_default: bool = True
    required_variables_json: List[str] = []

class AIPromptTemplateCreate(AIPromptTemplateBase):
    pass

class AIPromptTemplateResponse(AIPromptTemplateBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ----------------- Memory, Governance, & Audit Schemas -----------------
class AIMemoryStoreBase(BaseModel):
    tenant_id: Optional[uuid.UUID] = None
    memory_tier: MemoryTier
    session_id: Optional[str] = None
    case_id: Optional[uuid.UUID] = None
    investigation_id: Optional[uuid.UUID] = None
    key_name: str
    content_json: Dict[str, Any]
    is_compressed: bool = False
    compressed_summary: Optional[str] = None
    expires_at: Optional[datetime] = None

class AIMemoryStoreCreate(AIMemoryStoreBase):
    pass

class AIMemoryStoreResponse(AIMemoryStoreBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AIPolicyRuleBase(BaseModel):
    tenant_id: Optional[uuid.UUID] = None
    name: str
    rule_type: str
    description: Optional[str] = None
    allowed_models_json: List[str] = []
    blocked_keywords_json: List[str] = []
    require_human_review_threshold: float = 0.75
    pii_filtering_enabled: bool = True
    residency_region: str = "GLOBAL"
    is_active: bool = True

class AIPolicyRuleCreate(AIPolicyRuleBase):
    pass

class AIPolicyRuleResponse(AIPolicyRuleBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AIAuditLogResponse(BaseModel):
    id: uuid.UUID
    tenant_id: Optional[uuid.UUID] = None
    request_id: str
    user_id: Optional[uuid.UUID] = None
    provider_used: str
    model_used: str
    capability: Optional[str] = None
    confidence_score: float
    token_input_count: int
    token_output_count: int
    latency_ms: int
    status: str
    decision_trace_json: List[Any] = []
    timestamp: datetime
    hmac_signature: str

    model_config = ConfigDict(from_attributes=True)

class TokenUsageSummary(BaseModel):
    model: str
    total_input_tokens: int
    total_output_tokens: int
    total_cost_usd: float

    model_config = ConfigDict(from_attributes=True)
