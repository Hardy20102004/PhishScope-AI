import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

class ChainOfCustodyRecordBase(BaseModel):
    action_type: str
    actor_id: str
    timestamp: datetime
    notes: Optional[str]
    record_hash: str

class EvidenceItemBase(BaseModel):
    name: str
    source_type: str
    original_sha256: str
    acquisition_date: datetime
    acquired_by: str

class EvidenceItemResponse(EvidenceItemBase):
    id: uuid.UUID
    chain_of_custody: List[ChainOfCustodyRecordBase] = []
    model_config = ConfigDict(from_attributes=True)


class ReportSectionBase(BaseModel):
    section_type: str
    order_index: int
    content: str
    linked_evidence_ids: List[str]

class ForensicReportBase(BaseModel):
    title: str
    report_type: str

class ForensicReportCreate(ForensicReportBase):
    investigation_id: Optional[uuid.UUID] = None

class ForensicReportResponse(ForensicReportBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    investigation_id: Optional[uuid.UUID]
    created_at: datetime
    author_id: str
    is_finalized: bool
    digital_signature: Optional[str]
    
    sections: List[ReportSectionBase] = []
    
    model_config = ConfigDict(from_attributes=True)
