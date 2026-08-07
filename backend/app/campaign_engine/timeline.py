from sqlalchemy.orm import Session
from app.campaign_engine.models import CampaignTimeline
import uuid
from datetime import datetime, timezone

class CampaignTimelineEngine:
    """
    Manages the chronological sequence of events for a Campaign.
    """
    def __init__(self, db: Session):
        self.db = db

    def add_event(self, campaign_id: uuid.UUID, event_type: str, description: str, event_time: datetime = None) -> CampaignTimeline:
        """
        Adds a new event to the campaign timeline.
        """
        if not event_time:
            event_time = datetime.now(timezone.utc)
            
        event = CampaignTimeline(
            campaign_id=campaign_id,
            event_type=event_type,
            description=description,
            event_time=event_time
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_timeline(self, campaign_id: uuid.UUID):
        return self.db.query(CampaignTimeline).filter(CampaignTimeline.campaign_id == campaign_id).order_by(CampaignTimeline.event_time.asc()).all()
