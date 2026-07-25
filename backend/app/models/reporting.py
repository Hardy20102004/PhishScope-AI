import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum, JSON, Uuid, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base
import enum

class ReportStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class ExportFormat(str, enum.Enum):
    JSON = "JSON"
    CSV = "CSV"
    PDF = "PDF"
    HTML = "HTML"
    MARKDOWN = "MARKDOWN"
    ZIP = "ZIP"

class ReportTemplate(Base):
    __tablename__ = "report_templates"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    content_schema: Mapped[dict] = mapped_column(JSON, default=dict)
    html_template: Mapped[str] = mapped_column(Text, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    case_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=True, index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=True, index=True)
    template_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("report_templates.id"), nullable=True)
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    content_data: Mapped[dict] = mapped_column(JSON, default=dict)
    rendered_html: Mapped[str] = mapped_column(Text, nullable=True)
    
    status: Mapped[ReportStatus] = mapped_column(SQLEnum(ReportStatus), default=ReportStatus.DRAFT, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    created_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True)

class ExportRecord(Base):
    __tablename__ = "export_records"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    target_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), index=True, nullable=False) # Case ID or Investigation ID
    target_type: Mapped[str] = mapped_column(String, nullable=False) # "CASE" or "INVESTIGATION"
    
    format: Mapped[ExportFormat] = mapped_column(SQLEnum(ExportFormat), nullable=False)
    file_hash: Mapped[str] = mapped_column(String, nullable=True) # SHA-256
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True)

class EvidenceManifest(Base):
    __tablename__ = "evidence_manifests"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    case_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True)
    
    manifest_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    hash_value: Mapped[str] = mapped_column(String, nullable=False) # SHA-256 of the manifest_json
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_by: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True)
