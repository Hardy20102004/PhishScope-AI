from sqlalchemy import Column, String, JSON, Integer, Float, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime
import enum
import uuid

class PromptLifecycleState(str, enum.Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True, nullable=False, unique=True)
    category = Column(String, nullable=False)
    description = Column(String)
    owner = Column(String, default="system")
    is_active = Column(Boolean, default=True)
    
    versions = relationship("PromptVersion", back_populates="template", cascade="all, delete-orphan")

class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_id = Column(String, ForeignKey("prompt_templates.id"), nullable=False)
    version_number = Column(String, nullable=False) # e.g. "1.0.0"
    
    system_prompt = Column(String, nullable=False)
    user_template = Column(String, nullable=False)
    required_variables = Column(JSON, default=list)
    
    lifecycle_state = Column(String, default=PromptLifecycleState.DRAFT.value)
    
    template = relationship("PromptTemplate", back_populates="versions")

class PromptAnalyticsLog(Base):
    __tablename__ = "prompt_analytics_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    version_id = Column(String, ForeignKey("prompt_versions.id"), nullable=False)
    
    provider = Column(String, nullable=False) # e.g. "openai", "gemini"
    latency_ms = Column(Float, nullable=False)
    prompt_tokens = Column(Integer, nullable=False)
    completion_tokens = Column(Integer, nullable=False)
    total_cost = Column(Float, default=0.0)
    
    success = Column(Boolean, default=True)
    error_message = Column(String, nullable=True)
