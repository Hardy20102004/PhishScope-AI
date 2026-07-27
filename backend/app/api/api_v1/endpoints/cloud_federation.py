from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api import deps
from app.cloud import schemas, federation

router = APIRouter()

@router.post("/nodes", response_model=schemas.FederationNodeResponse)
def register_node(node: schemas.FederationNodeCreate, db: Session = Depends(deps.get_db)):
    engine = federation.FederationEngine(db)
    return engine.register_node(node.name, node.url, node.node_type, node.auth_method)

@router.get("/nodes", response_model=List[schemas.FederationNodeResponse])
def list_nodes(db: Session = Depends(deps.get_db)):
    engine = federation.FederationEngine(db)
    return engine.list_nodes()

@router.post("/nodes/{node_id}/pull", response_model=schemas.FederationSyncResponse)
def pull_sync(node_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    engine = federation.FederationEngine(db)
    try:
        return engine.trigger_pull_sync(node_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/nodes/{node_id}/push", response_model=schemas.FederationSyncResponse)
def push_sync(node_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    engine = federation.FederationEngine(db)
    try:
        return engine.trigger_push_sync(node_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
