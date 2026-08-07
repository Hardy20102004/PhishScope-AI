from typing import Optional, List
import structlog
from sqlalchemy.orm import Session

from app.models.timeline import Timeline, ThreatTimelineEvent, EventEvidence
from app.schemas.timeline import TimelineCreate, ThreatTimelineEventCreate

logger = structlog.get_logger("phoenix.timeline.manager")

class TimelineManager:
    """Handles CRUD operations for Timelines and Events."""
    def __init__(self, db: Session):
        self.db = db

    def create_timeline(self, req: TimelineCreate) -> Timeline:
        timeline = Timeline(
            name=req.name,
            description=req.description,
            timeline_type=req.timeline_type,
            tenant_id=req.tenant_id
        )
        self.db.add(timeline)
        self.db.commit()
        self.db.refresh(timeline)
        return timeline

    def get_timeline(self, timeline_id: str) -> Optional[Timeline]:
        return self.db.query(Timeline).filter_by(id=timeline_id).first()

    def get_all_timelines(self, tenant_id: Optional[str] = None) -> List[Timeline]:
        q = self.db.query(Timeline)
        if tenant_id:
            q = q.filter_by(tenant_id=tenant_id)
        return q.all()

    def add_event(self, timeline_id: str, req: ThreatTimelineEventCreate) -> ThreatTimelineEvent:
        event = ThreatTimelineEvent(
            timeline_id=timeline_id,
            timestamp=req.timestamp,
            title=req.title,
            description=req.description,
            category=req.category,
            entity_id=req.entity_id,
            confidence=req.confidence,
            is_hypothetical=req.is_hypothetical,
            properties_json=req.properties_json
        )
        self.db.add(event)
        
        if req.evidence:
            for ev_req in req.evidence:
                ev = EventEvidence(
                    event=event,
                    source_type=ev_req.source_type,
                    reference_url=ev_req.reference_url,
                    snippet=ev_req.snippet
                )
                self.db.add(ev)
                
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_timeline_events(self, timeline_id: str) -> List[ThreatTimelineEvent]:
        """Returns all events for a timeline, sorted chronologically."""
        return self.db.query(ThreatTimelineEvent).filter_by(timeline_id=timeline_id).order_by(ThreatTimelineEvent.timestamp.asc()).all()
