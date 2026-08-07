import structlog
from datetime import datetime, timezone
from dateutil import parser
from app.schemas.timeline import ThreatTimelineEventCreate
from app.models.timeline import EventCategory

logger = structlog.get_logger("phoenix.timeline.builder")

class EventNormalizationEngine:
    """Normalizes raw data into standard timeline events."""
    
    @staticmethod
    def normalize_timestamp(raw_date: str) -> datetime:
        """Parses various date strings into a UTC datetime object."""
        try:
            dt = parser.parse(raw_date)
            # Ensure it is timezone aware, then convert to UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception as e:
            logger.error("timestamp_normalization_failed", raw_date=raw_date, error=str(e))
            return datetime.now(timezone.utc)

class TimelineBuilder:
    """Builds timelines from various sources."""
    
    @staticmethod
    def build_from_stix(stix_bundle: dict) -> list[ThreatTimelineEventCreate]:
        """Parses a STIX bundle and converts Sightings/Relationships to ThreatTimelineEvents."""
        events = []
        for obj in stix_bundle.get("objects", []):
            if obj.get("type") == "sighting":
                dt = EventNormalizationEngine.normalize_timestamp(obj.get("first_seen", obj.get("created")))
                events.append(ThreatTimelineEventCreate(
                    timestamp=dt,
                    title=f"Sighting of {obj.get('sighting_of_ref', 'Unknown')}",
                    category=EventCategory.OBSERVATION,
                    description=obj.get("description"),
                    confidence=0.8
                ))
        return events
