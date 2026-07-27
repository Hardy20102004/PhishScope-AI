from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api import deps
from app.cloud import schemas, workspace_manager
from app.cloud.models import WorkspaceType

router = APIRouter()

@router.post("/", response_model=schemas.WorkspaceResponse)
def create_workspace(workspace: schemas.WorkspaceCreate, db: Session = Depends(deps.get_db)):
    manager = workspace_manager.WorkspaceManager(db)
    try:
        return manager.create_workspace(workspace.tenant_id, workspace.name, workspace.workspace_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tenant/{tenant_id}", response_model=List[schemas.WorkspaceResponse])
def list_workspaces(tenant_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    manager = workspace_manager.WorkspaceManager(db)
    return manager.list_workspaces(tenant_id)

@router.post("/{workspace_id}/members", response_model=schemas.WorkspaceMemberResponse)
def add_member(workspace_id: uuid.UUID, member: schemas.WorkspaceMemberCreate, db: Session = Depends(deps.get_db)):
    manager = workspace_manager.WorkspaceManager(db)
    try:
        return manager.add_member(workspace_id, member.user_id, member.role)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{workspace_id}/members", response_model=List[schemas.WorkspaceMemberResponse])
def list_members(workspace_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    manager = workspace_manager.WorkspaceManager(db)
    return manager.get_members(workspace_id)
