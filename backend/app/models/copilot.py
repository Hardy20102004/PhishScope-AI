import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class MessageRole(str, enum.Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "ASSISTANT"

class CopilotSessionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

class CodeReviewStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class DeveloperCopilotSession(Base):
    """
    Tracks an active developer assistant session.
    """
    __tablename__ = "dev_copilot_sessions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    developer_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    repository_context: Mapped[str] = mapped_column(String(1024), nullable=True)
    environment: Mapped[str] = mapped_column(String(50), default="VS_CODE")
    status: Mapped[CopilotSessionStatus] = mapped_column(Enum(CopilotSessionStatus), default=CopilotSessionStatus.ACTIVE)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CodeReviewRecord(Base):
    """
    Represents an AI-driven secure code review event (e.g., triggered on a PR).
    """
    __tablename__ = "copilot_code_reviews"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    repository_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    pull_request_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    commit_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    status: Mapped[CodeReviewStatus] = mapped_column(Enum(CodeReviewStatus), default=CodeReviewStatus.PENDING)
    
    findings_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class CodeReviewFinding(Base):
    """
    A specific architectural or secure coding recommendation.
    """
    __tablename__ = "copilot_review_findings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    review_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("copilot_code_reviews.id", ondelete="CASCADE"), index=True)
    
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    line_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM")
    cwe_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    suggestion: Mapped[str] = mapped_column(Text, nullable=False) # The AI's proposed code change

class DeveloperLearningProgress(Base):
    """
    Tracks a developer's engagement with contextual security guidance.
    """
    __tablename__ = "copilot_learning_progress"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    developer_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    topic: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. "OWASP A01: Broken Access Control"
    modules_completed: Mapped[int] = mapped_column(Integer, default=0)
    
    last_engaged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EngineeringMetric(Base):
    """
    Stores aggregated project-level intelligence.
    """
    __tablename__ = "copilot_engineering_metrics"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    technical_debt_score: Mapped[float] = mapped_column(Float, default=0.0) # 0-100 scale
    security_trend_score: Mapped[float] = mapped_column(Float, default=0.0) # Positive is improving
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CopilotConversation(Base):
    __tablename__ = "copilot_conversations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    messages: Mapped[list["CopilotMessage"]] = relationship("CopilotMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="CopilotMessage.created_at")

class CopilotMessage(Base):
    __tablename__ = "copilot_messages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("copilot_conversations.id", ondelete="CASCADE"), index=True, nullable=False)
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Store evidence citations (e.g., {"url": "...", "finding_id": "..."})
    evidence_references: Mapped[list] = mapped_column(JSON, default=list)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    conversation: Mapped["CopilotConversation"] = relationship("CopilotConversation", back_populates="messages")

class GeneratedReport(Base):
    __tablename__ = "generated_reports"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=False)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False) # Executive, Technical, etc.
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    generated_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
