import uuid
from datetime import datetime, timezone
import enum
from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum, JSON, Uuid, Text, Boolean, Float, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base

class ProviderType(str, enum.Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"
    MISTRAL = "mistral"
    DEEPSEEK = "deepseek"
    QWEN = "qwen"
    LLAMA = "llama"
    OLLAMA = "ollama"
    ENTERPRISE_LOCAL = "enterprise_local"
    CUSTOM = "custom"

class ModelHealthStatus(str, enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNREACHABLE = "UNREACHABLE"
    OFFLINE = "OFFLINE"

class MemoryTier(str, enum.Enum):
    SESSION = "SESSION"
    CASE = "CASE"
    CONVERSATION = "CONVERSATION"
    EVIDENCE = "EVIDENCE"
    ORGANIZATION = "ORGANIZATION"
    USER_PREF = "USER_PREF"

class AIProviderConfig(Base):
    __tablename__ = "ai_provider_configs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    provider_type: Mapped[ProviderType] = mapped_column(SQLEnum(ProviderType), nullable=False)
    base_url: Mapped[str] = mapped_column(String, nullable=True)
    api_key_encrypted: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=100, nullable=False) # Lower integer = higher priority in failover
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    models: Mapped[list["AIModelEntry"]] = relationship("AIModelEntry", back_populates="provider_config", cascade="all, delete-orphan")

class AIModelEntry(Base):
    __tablename__ = "ai_model_entries"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    provider_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("ai_provider_configs.id", ondelete="CASCADE"), index=True, nullable=False)
    model_id: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True) # e.g. "gpt-4o", "gemini-3.1-pro", "claude-3-5-sonnet"
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=True)
    max_context_tokens: Mapped[int] = mapped_column(Integer, default=128000, nullable=False)
    max_output_tokens: Mapped[int] = mapped_column(Integer, default=4096, nullable=False)
    supported_languages: Mapped[list] = mapped_column(JSON, default=lambda: ["en", "es", "fr", "de", "zh", "ja"])
    cost_per_1k_input_usd: Mapped[float] = mapped_column(Float, default=0.003, nullable=False)
    cost_per_1k_output_usd: Mapped[float] = mapped_column(Float, default=0.015, nullable=False)
    typical_latency_ms: Mapped[int] = mapped_column(Integer, default=800, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    health_status: Mapped[ModelHealthStatus] = mapped_column(SQLEnum(ModelHealthStatus), default=ModelHealthStatus.HEALTHY, nullable=False)
    capabilities_json: Mapped[list] = mapped_column(JSON, default=list) # e.g. ["Summarization", "Threat Analysis", "Reasoning"]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    provider_config: Mapped["AIProviderConfig"] = relationship("AIProviderConfig", back_populates="models")

class AICapabilityMapping(Base):
    __tablename__ = "ai_capability_mappings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    capability_name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True) # e.g. "Threat Analysis"
    description: Mapped[str] = mapped_column(Text, nullable=True)
    default_model_id: Mapped[str] = mapped_column(String, nullable=False)
    fallback_model_ids_json: Mapped[list] = mapped_column(JSON, default=list)
    parameters_json: Mapped[dict] = mapped_column(JSON, default=lambda: {"temperature": 0.2, "top_p": 0.95})
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AIPromptTemplate(Base):
    __tablename__ = "ai_prompt_templates"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True) # e.g. "Threat Analysis", "Executive Summary"
    description: Mapped[str] = mapped_column(Text, nullable=True)
    template_type: Mapped[str] = mapped_column(String, nullable=False, index=True) # Executive Summary, Technical Summary, etc.
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    user_template: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(String, default="1.0.0", nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    required_variables_json: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AIMemoryStore(Base):
    __tablename__ = "ai_memory_store"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    memory_tier: Mapped[MemoryTier] = mapped_column(SQLEnum(MemoryTier), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    case_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    key_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    is_compressed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    compressed_summary: Mapped[str] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AIPolicyRule(Base):
    __tablename__ = "ai_policy_rules"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    rule_type: Mapped[str] = mapped_column(String, nullable=False) # e.g. "MODEL_RESTRICT", "PII_MASKING", "RESIDENCY"
    description: Mapped[str] = mapped_column(Text, nullable=True)
    allowed_models_json: Mapped[list] = mapped_column(JSON, default=list)
    blocked_keywords_json: Mapped[list] = mapped_column(JSON, default=list)
    require_human_review_threshold: Mapped[float] = mapped_column(Float, default=0.75, nullable=False)
    pii_filtering_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    residency_region: Mapped[str] = mapped_column(String, default="GLOBAL", nullable=False) # e.g. "US", "EU", "LOCAL_ONLY"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AIAuditLogRecord(Base):
    __tablename__ = "ai_audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    request_id: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    provider_used: Mapped[str] = mapped_column(String, nullable=False)
    model_used: Mapped[str] = mapped_column(String, nullable=False)
    capability: Mapped[str] = mapped_column(String, nullable=True)
    input_prompt_encrypted: Mapped[str] = mapped_column(Text, nullable=False) # AES-256 GCM payload
    output_response_encrypted: Mapped[str] = mapped_column(Text, nullable=False) # AES-256 GCM payload
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    token_input_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    token_output_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String, default="SUCCESS", nullable=False) # SUCCESS, FAILOVER, POLICY_VIOLATION, ERROR
    decision_trace_json: Mapped[list] = mapped_column(JSON, default=list)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    hmac_signature: Mapped[str] = mapped_column(String, nullable=False) # HMAC integrity chaining

class TokenUsageRecord(Base):
    __tablename__ = "token_usage_records"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    model: Mapped[str] = mapped_column(String, nullable=False, index=True)
    date_bucket: Mapped[str] = mapped_column(String, nullable=False, index=True) # e.g. "2026-07-25"
    total_input_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_output_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
