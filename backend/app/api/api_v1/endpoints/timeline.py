from typing import List, Any, Dict
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api import deps
from app.timeline.manager import TimelineManager
from app.timeline.analytics import TimelineAnalyticsEngine
from app.timeline.correlation import HistoricalReconstructionEngine
from app.schemas.timeline import (
    TimelineCreate,
    TimelineResponse,
    ThreatTimelineEventCreate,
    ThreatTimelineEventResponse
)

router = APIRouter()

@router.post("/", response_model=TimelineResponse)
def create_timeline(req: TimelineCreate, db: Session = Depends(deps.get_db)):
    manager = TimelineManager(db)
    return manager.create_timeline(req)

@router.get("/", response_model=List[TimelineResponse])
def get_timelines(tenant_id: str = None, db: Session = Depends(deps.get_db)):
    manager = TimelineManager(db)
    return manager.get_all_timelines(tenant_id=tenant_id)

@router.get("/{timeline_id}", response_model=TimelineResponse)
def get_timeline(timeline_id: str, db: Session = Depends(deps.get_db)):
    manager = TimelineManager(db)
    timeline = manager.get_timeline(timeline_id)
    if not timeline:
        raise HTTPException(status_code=404, detail="Timeline not found")
    
    # Attach events for full response
    events = manager.get_timeline_events(timeline_id)
    timeline.events = events
    return timeline

@router.post("/{timeline_id}/events", response_model=ThreatTimelineEventResponse)
def add_event(timeline_id: str, req: ThreatTimelineEventCreate, db: Session = Depends(deps.get_db)):
    manager = TimelineManager(db)
    return manager.add_event(timeline_id, req)

@router.post("/{timeline_id}/reconstruct")
def trigger_historical_reconstruction(timeline_id: str, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)):
    """Triggers asynchronous historical reconstruction."""
    def reconstruct_task(t_id: str):
        from app.db.session import SessionLocal
        bg_db = SessionLocal()
        try:
            engine = HistoricalReconstructionEngine(bg_db)
            engine.reconstruct(t_id)
        finally:
            bg_db.close()
            
    background_tasks.add_task(reconstruct_task, timeline_id)
    return {"status": "success", "message": "Historical reconstruction started in background."}

@router.get("/{timeline_id}/analytics/heatmap", response_model=List[Dict[str, Any]])
def get_timeline_heatmap(timeline_id: str, db: Session = Depends(deps.get_db)):
    engine = TimelineAnalyticsEngine(db)
    return engine.generate_density_heatmap(timeline_id)
