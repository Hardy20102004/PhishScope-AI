import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.case_management import TimelineEvent


class TimelineEngine:
    def __init__(self, db: Session):
        self.db = db
        
    def add_event(self, case_id: uuid.UUID, action: str, details: Optional[str] = None, metadata: dict = None, user_id: Optional[uuid.UUID] = None) -> TimelineEvent:
        event = TimelineEvent(
            case_id=case_id,
            user_id=user_id,
            action=action,
            details=details,
            metadata_json=metadata or {}
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
