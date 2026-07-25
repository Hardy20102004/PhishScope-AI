from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from pydantic import BaseModel

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.reporting import (
    ReportCreate, ReportUpdate, ReportSchema,
    ExportRequest, ExportRecordSchema, EvidenceManifestSchema
)
from app.services.reporting_engine import ReportingEngine
from app.services.export_service import ExportService
from app.services.custody_service import CustodyService

router = APIRouter()

@router.get("/", response_model=List[ReportSchema])
def list_reports(
    case_id: UUID = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ReportingEngine(db)
    return engine.list_reports(case_id=case_id)

@router.post("/generate", response_model=ReportSchema)
def create_report(
    request: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = ReportingEngine(db)
    return engine.create_report(request, current_user.id)

@router.patch("/{report_id}/status", response_model=ReportSchema)
def update_report(
    report_id: UUID,
    request: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        engine = ReportingEngine(db)
        return engine.update_report(report_id, request, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/cases/{case_id}/export", response_model=ExportRecordSchema)
def export_case(
    case_id: UUID,
    request: ExportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        engine = ExportService(db)
        return engine.generate_case_export(case_id, request.format, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/cases/{case_id}/manifest", response_model=EvidenceManifestSchema)
def generate_manifest(
    case_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        engine = CustodyService(db)
        return engine.generate_manifest(case_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

class VerifyRequest(BaseModel):
    manifest_json: dict
    hash_value: str

@router.post("/verify")
def verify_manifest(
    request: VerifyRequest,
    db: Session = Depends(get_db)
):
    engine = CustodyService(db)
    is_valid = engine.verify_manifest(request.manifest_json, request.hash_value)
    return {"valid": is_valid}
