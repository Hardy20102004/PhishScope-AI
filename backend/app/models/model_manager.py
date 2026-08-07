import uuid
from typing import Optional
from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AIProvider(Base):
    """
    e.g., OpenAI, Anthropic, Ollama
    """
    __tablename__ = "ai_providers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    base_url = Column(String, nullable=True)
    api_key_secret = Column(String, nullable=True) # Mocked reference to Vault/env
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    models = relationship("AIModel", back_populates="provider", cascade="all, delete-orphan")

class AIModel(Base):
    """
    e.g., gpt-4o, claude-3-opus
    """
    __tablename__ = "ai_models"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider_id = Column(String, ForeignKey("ai_providers.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    
    capabilities = Column(JSON, default=list) # e.g. ["THREAT_ANALYSIS", "REASONING"]
    context_window = Column(Integer, nullable=False, default=8192)
    
    # Costs per 1k tokens
    cost_per_1k_prompt = Column(Float, nullable=False, default=0.0)
    cost_per_1k_completion = Column(Float, nullable=False, default=0.0)
    
    is_active = Column(Boolean, default=True)
    health_status = Column(String, default="HEALTHY")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    provider = relationship("AIProvider", back_populates="models")


class RoutingPolicy(Base):
    """
    Maps a specific task/capability to a primary and fallback model.
    """
    __tablename__ = "ai_routing_policies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    capability = Column(String, nullable=False, unique=True, index=True) # e.g. "THREAT_ANALYSIS"
    
    primary_model_id = Column(String, ForeignKey("ai_models.id", ondelete="SET NULL"), nullable=True)
    fallback_model_id = Column(String, ForeignKey("ai_models.id", ondelete="SET NULL"), nullable=True)
    
    max_cost_limit = Column(Float, nullable=True) # Optional budget limit per execution
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    primary_model = relationship("AIModel", foreign_keys=[primary_model_id])
    fallback_model = relationship("AIModel", foreign_keys=[fallback_model_id])

class ModelCostLog(Base):
    """
    Global ledger for token usage and cost.
    """
    __tablename__ = "ai_cost_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=True, index=True)
    model_id = Column(String, ForeignKey("ai_models.id", ondelete="SET NULL"), nullable=True)
    
    task_type = Column(String, nullable=False)
    
    prompt_tokens = Column(Integer, nullable=False, default=0)
    completion_tokens = Column(Integer, nullable=False, default=0)
    total_cost = Column(Float, nullable=False, default=0.0)
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    model = relationship("AIModel")
