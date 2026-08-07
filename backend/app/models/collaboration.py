import uuid
from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

# Association table for Workspace Members
workspace_members = Table(
    "collab_workspace_members",
    Base.metadata,
    Column("workspace_id", ForeignKey("collab_workspaces.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)

class CollabWorkspace(Base):
    __tablename__ = "collab_workspaces"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), index=True)
    workspace_type: Mapped[str] = mapped_column(String(50)) # INCIDENT, HUNT, GENERAL
    linked_entity_id: Mapped[Optional[uuid.UUID]] = mapped_column(nullable=True, index=True) # ID of the Incident or Hunt
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    messages = relationship("ChatMessage", back_populates="workspace", cascade="all, delete-orphan")
    notes = relationship("AnalystNote", back_populates="workspace", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "collab_chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collab_workspaces.id", ondelete="CASCADE"), index=True)
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    content: Mapped[str] = mapped_column(Text)
    is_system_message: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    workspace = relationship("CollabWorkspace", back_populates="messages")


class AnalystNote(Base):
    __tablename__ = "collab_analyst_notes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    workspace_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("collab_workspaces.id", ondelete="CASCADE"), nullable=True, index=True)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text) # Markdown
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    workspace = relationship("CollabWorkspace", back_populates="notes")


class AnalystPresence(Base):
    __tablename__ = "collab_analyst_presence"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    
    status: Mapped[str] = mapped_column(String(50), default="ONLINE") # ONLINE, BUSY, OFFLINE
    active_cases: Mapped[int] = mapped_column(Integer, default=0)
    
    last_active: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
