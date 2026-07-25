import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum, JSON, Uuid, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
import enum

class MessageRole(str, enum.Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"

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
    role: Mapped[MessageRole] = mapped_column(SQLEnum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Store evidence citations (e.g., {"url": "...", "finding_id": "..."})
    evidence_references: Mapped[list] = mapped_column(JSON, default=list)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    conversation: Mapped["CopilotConversation"] = relationship("CopilotConversation", back_populates="messages")

class GeneratedReport(Base):
    __tablename__ = "generated_reports"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=False)
    report_type: Mapped[str] = mapped_column(String, nullable=False) # Executive, Technical, etc.
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    generated_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
