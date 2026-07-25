from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.automation import Workflow, WorkflowVersion, WorkflowExecution
from app.schemas.automation import (
    WorkflowCreate, WorkflowUpdate, WorkflowSchema,
    WorkflowExecutionSchema, WorkflowVersionBase
)
from app.services.automation.execution_engine import ExecutionEngine

router = APIRouter()

@router.get("/workflows", response_model=List[WorkflowSchema])
def list_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Workflow).order_by(Workflow.created_at.desc())
    return list(db.execute(stmt).scalars().all())

@router.post("/workflows", response_model=WorkflowSchema)
def create_workflow(
    request: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = Workflow(
        name=request.name,
        description=request.description,
        trigger_type=request.trigger_type,
        is_active=request.is_active
    )
    db.add(workflow)
    db.flush()
    
    version = WorkflowVersion(
        workflow_id=workflow.id,
        version_number=1,
        definition_json=request.definition_json,
        created_by=current_user.id
    )
    db.add(version)
    db.commit()
    db.refresh(workflow)
    return workflow

@router.post("/workflows/{workflow_id}/execute", response_model=WorkflowExecutionSchema)
def execute_workflow(
    workflow_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get latest version
    stmt = select(WorkflowVersion).where(WorkflowVersion.workflow_id == workflow_id).order_by(WorkflowVersion.version_number.desc()).limit(1)
    version = db.execute(stmt).scalar_one_or_none()
    if not version:
        raise HTTPException(status_code=404, detail="Workflow version not found")
        
    engine = ExecutionEngine(db)
    
    # Run sync for immediate feedback in this API
    execution = engine.start_execution(version.id, payload)
    engine.run_workflow_sync(execution.id)
    
    db.refresh(execution)
    return execution

@router.get("/executions/{execution_id}", response_model=WorkflowExecutionSchema)
def get_execution(
    execution_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(WorkflowExecution).where(WorkflowExecution.id == execution_id)
    execution = db.execute(stmt).scalar_one_or_none()
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution
