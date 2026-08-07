from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.reporting import ExportFormat, ReportStatus


class ReportTemplateSchema(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    content_schema: dict
    html_template: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ReportCreate(BaseModel):
    title: str
    template_id: Optional[UUID] = None
    case_id: Optional[UUID] = None
    investigation_id: Optional[UUID] = None
    content_data: dict = {}

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    content_data: Optional[dict] = None
    status: Optional[ReportStatus] = None

class ReportSchema(BaseModel):
    id: UUID
    title: str
    case_id: Optional[UUID]
    investigation_id: Optional[UUID]
    template_id: Optional[UUID]
    content_data: dict
    rendered_html: Optional[str]
    status: ReportStatus
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID]
    approved_by: Optional[UUID]

    model_config = ConfigDict(from_attributes=True)

class ExportRequest(BaseModel):
    format: ExportFormat
    include_evidence: bool = True

class EvidenceManifestSchema(BaseModel):
    id: UUID
    case_id: UUID
    manifest_json: dict
    hash_value: str
    created_at: datetime
    created_by: Optional[UUID]
    
    model_config = ConfigDict(from_attributes=True)

class ExportRecordSchema(BaseModel):
    id: UUID
    target_id: UUID
    target_type: str
    format: ExportFormat
    file_hash: Optional[str]
    created_at: datetime
    created_by: Optional[UUID]

    model_config = ConfigDict(from_attributes=True)
