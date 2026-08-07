from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from loguru import logger

from app.api import deps
from app.ti_feed.schemas import (
    FeedRegistryCreate,
    FeedRegistryUpdate,
    FeedRegistryResponse,
    FeedAnalytics
)
from app.ti_feed.models import FeedRegistry, FeedVersion
from app.ti_feed.scheduler import FeedScheduler

router = APIRouter()

@router.post("/registry", response_model=FeedRegistryResponse, status_code=status.HTTP_201_CREATED)
def create_feed(
    *,
    db: Session = Depends(deps.get_db),
    feed_in: FeedRegistryCreate,
) -> Any:
    """
    Register a new Threat Intelligence Feed.
    """
    feed = FeedRegistry(**feed_in.model_dump())
    db.add(feed)
    db.commit()
    db.refresh(feed)
    return feed

@router.get("/registry", response_model=List[FeedRegistryResponse])
def get_feeds(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    List all registered feeds.
    """
    feeds = db.query(FeedRegistry).offset(skip).limit(limit).all()
    return feeds

@router.post("/{feed_id}/sync")
def sync_feed(
    feed_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Manually trigger a synchronization for a specific feed.
    Runs asynchronously.
    """
    feed = db.query(FeedRegistry).filter(FeedRegistry.id == feed_id).first()
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
        
    scheduler = FeedScheduler(db)
    # Using background tasks for fast API response, ideally Celery
    background_tasks.add_task(scheduler.sync_feed, str(feed_id))
    
    return {"message": "Synchronization started in the background", "feed_id": feed_id}

@router.get("/analytics/summary", response_model=FeedAnalytics)
def get_feed_analytics(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get high-level analytics for the Threat Intelligence Feed Platform.
    """
    total_feeds = db.query(FeedRegistry).count()
    active_feeds = db.query(FeedRegistry).filter(FeedRegistry.status == "Active").count()
    
    # Calculate indicators ingested from FeedVersions
    total_indicators_row = db.query(db.func.sum(FeedVersion.indicators_added)).first()
    total_indicators = int(total_indicators_row[0]) if total_indicators_row and total_indicators_row[0] is not None else 0
    
    return FeedAnalytics(
        total_feeds=total_feeds,
        active_feeds=active_feeds,
        total_indicators_ingested=total_indicators,
        sync_success_rate=98.5, # Mock metric
        recent_errors=0, # Mock metric
        feeds_by_format={"STIX 2.1": 2, "CSV": 1} # Mock metric
    )
