import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class CopilotSession(Base):
    __tablename__ = "soc_copilot_sessions"
    """
    A global conversation thread, decoupled from any specific incident.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255), default="New Conversation")
    context_tags: Mapped[dict] = mapped_column(JSON, default=list) # e.g., ["Threat Hunting", "APT29"]
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    messages = relationship("CopilotChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="CopilotChatMessage.created_at")
    reasoning_logs = relationship("CopilotReasoningLog", back_populates="session", cascade="all, delete-orphan")


class CopilotChatMessage(Base):
    __tablename__ = "soc_copilot_messages"
    """
    Tracks messages within a session.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("soc_copilot_sessions.id", ondelete="CASCADE"), index=True)
    
    role: Mapped[str] = mapped_column(String(50)) # USER, ASSISTANT, SYSTEM
    content: Mapped[str] = mapped_column(Text)
    evidence_citations: Mapped[dict] = mapped_column(JSON, default=list) # Citations used by AI
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    session = relationship("CopilotSession", back_populates="messages")


class CopilotReasoningLog(Base):
    __tablename__ = "soc_copilot_reasoning"
    """
    Stores the chain-of-thought logic (evidence vs analytical assessment) for explainable AI auditing.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("soc_copilot_sessions.id", ondelete="CASCADE"), index=True)
    message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("soc_copilot_messages.id", ondelete="CASCADE"), index=True)
    
    observed_evidence: Mapped[dict] = mapped_column(JSON, default=list)
    analytical_assessment: Mapped[str] = mapped_column(Text)
    confidence_score: Mapped[float] = mapped_column(default=0.0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    session = relationship("CopilotSession", back_populates="reasoning_logs")
