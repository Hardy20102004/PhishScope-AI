import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class Mailbox(Base):
    __tablename__ = "mf_mailboxes"
    """
    Metadata about an acquired email container (PST, MBOX, EML collection).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=True)
    
    name: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(String(50)) # PST, EML, M365_Export
    owner_email: Mapped[str] = mapped_column(String(255), nullable=True)
    
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    messages = relationship("EmailMessage", back_populates="mailbox", cascade="all, delete-orphan")


class EmailMessage(Base):
    __tablename__ = "mf_email_messages"
    """
    Core message data extracted from the container.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    mailbox_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_mailboxes.id", ondelete="CASCADE"), index=True)
    
    message_id_header: Mapped[str] = mapped_column(String(255), index=True, nullable=True)
    subject: Mapped[str] = mapped_column(Text, nullable=True)
    sender: Mapped[str] = mapped_column(String(255))
    recipients: Mapped[str] = mapped_column(Text) # Comma separated
    
    body_text: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Forensic Flags
    is_phishing_suspect: Mapped[bool] = mapped_column(Boolean, default=False)
    auth_pass: Mapped[bool] = mapped_column(Boolean, default=True) # SPF/DKIM/DMARC status
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    mailbox = relationship("Mailbox", back_populates="messages")
    headers = relationship("EmailHeader", back_populates="message", cascade="all, delete-orphan")


class EmailHeader(Base):
    __tablename__ = "mf_email_headers"
    """
    Granular key-value pair extracted from the raw MIME header.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_email_messages.id", ondelete="CASCADE"), index=True)
    
    header_name: Mapped[str] = mapped_column(String(100), index=True) # e.g., Received, Authentication-Results
    header_value: Mapped[str] = mapped_column(Text)
    
    # For 'Received' headers, extracting the chronological hop
    hop_index: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # For structured JSON analysis by engines (e.g., {"spf": "pass", "dkim": "fail"})
    parsed_data: Mapped[dict] = mapped_column(JSON, nullable=True) 
    
    message = relationship("EmailMessage", back_populates="headers")
