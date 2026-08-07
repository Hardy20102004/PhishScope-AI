from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api import deps
from app.cloud import schemas, analytics_engine

router = APIRouter()

@router.post("/generate", response_model=schemas.CloudAnalyticsResponse)
def generate_metrics(db: Session = Depends(deps.get_db)):
    engine = analytics_engine.AnalyticsEngine(db)
    return engine.generate_sharing_volume_metric()

@router.get("/metrics", response_model=List[schemas.CloudAnalyticsResponse])
def get_metrics(limit: int = 10, db: Session = Depends(deps.get_db)):
    engine = analytics_engine.AnalyticsEngine(db)
    return engine.get_latest_metrics(limit)
