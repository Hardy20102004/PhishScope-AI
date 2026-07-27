from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api import deps
from app.cloud import sync_engine

router = APIRouter()

@router.post("/full/{node_id}")
def trigger_full_sync(node_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    engine = sync_engine.SynchronizationEngine(db)
    try:
        success = engine.trigger_full_sync(node_id)
        return {"status": "success" if success else "queued_for_offline"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/incremental/{node_id}")
def trigger_incremental_sync(node_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    engine = sync_engine.SynchronizationEngine(db)
    try:
        record = engine.trigger_incremental_sync(node_id)
        return record
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
