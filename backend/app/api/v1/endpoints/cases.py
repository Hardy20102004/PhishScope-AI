from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.case_management import (
    CaseCreate,
    CaseSchema,
    CaseTaskCreate,
    CaseTaskSchema,
    CaseTaskUpdate,
    CaseUpdate,
    DecisionLogCreate,
    DecisionLogSchema,
)
from app.services.case_engine import CaseEngine
from app.services.task_engine import TaskEngine

router = APIRouter()

@router.get("/", response_model=List[CaseSchema])
def list_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = CaseEngine(db)
    return engine.list_cases()

@router.post("/", response_model=CaseSchema)
def create_case(
    request: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = CaseEngine(db)
    case = engine.create_case(request, current_user.id)
    return case

@router.get("/{case_id}", response_model=CaseSchema)
def get_case(
    case_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        engine = CaseEngine(db)
        return engine.get_case(case_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{case_id}", response_model=CaseSchema)
def update_case(
    case_id: UUID,
    request: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        engine = CaseEngine(db)
        return engine.update_case(case_id, request, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{case_id}/tasks", response_model=CaseTaskSchema)
def add_task(
    case_id: UUID,
    request: CaseTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = TaskEngine(db)
    return engine.add_task(case_id, request, current_user.id)

@router.patch("/{case_id}/tasks/{task_id}", response_model=CaseTaskSchema)
def update_task(
    case_id: UUID,
    task_id: UUID,
    request: CaseTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        engine = TaskEngine(db)
        return engine.update_task_status(task_id, request.status, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{case_id}/decisions", response_model=DecisionLogSchema)
def record_decision(
    case_id: UUID,
    request: DecisionLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    engine = CaseEngine(db)
    return engine.record_decision(case_id, request, current_user.id)

@router.post("/{case_id}/link-investigation/{investigation_id}")
def link_investigation(
    case_id: UUID,
    investigation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        engine = CaseEngine(db)
        engine.link_investigation(case_id, investigation_id, current_user.id)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
