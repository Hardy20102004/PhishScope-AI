from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api import deps
from app.cloud import schemas, sharing_engine
from app.cloud.models import TLPLevel

router = APIRouter()

@router.post("/policies", response_model=schemas.SharingPolicyResponse)
def create_policy(policy: schemas.SharingPolicyCreate, workspace_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    engine = sharing_engine.SharingEngine(db)
    return engine.create_policy(workspace_id, policy.name, policy.tlp_level, policy.require_approval, policy.target_audiences)

@router.get("/policies/{workspace_id}", response_model=List[schemas.SharingPolicyResponse])
def list_policies(workspace_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    engine = sharing_engine.SharingEngine(db)
    return engine.get_policies(workspace_id)

@router.post("/share", response_model=schemas.SharedObjectResponse)
def share_object(
    workspace_id: uuid.UUID,
    obj: schemas.SharedObjectCreate,
    current_user_id: uuid.UUID = uuid.UUID("00000000-0000-0000-0000-000000000000"), # Mock user ID for now
    db: Session = Depends(deps.get_db)
):
    engine = sharing_engine.SharingEngine(db)
    try:
        return engine.share_object(workspace_id, obj.entity_type, obj.entity_id, obj.payload, obj.tlp_level, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
