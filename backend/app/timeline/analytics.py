from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
import structlog
from app.models.timeline import ThreatTimelineEvent

logger = structlog.get_logger("phoenix.timeline.analytics")

class TimelineAnalyticsEngine:
    def __init__(self, db: Session):
        self.db = db

    def generate_density_heatmap(self, timeline_id: str) -> List[Dict[str, Any]]:
        """
        Calculates event frequency per day to power the UI Heatmap.
        """
        events = self.db.query(ThreatTimelineEvent.timestamp).filter_by(timeline_id=timeline_id).all()
        
        # Aggregate by YYYY-MM-DD
        heatmap = {}
        for (ts,) in events:
            date_str = ts.strftime('%Y-%m-%d')
            heatmap[date_str] = heatmap.get(date_str, 0) + 1
            
        result = [{"date": k, "count": v} for k, v in heatmap.items()]
        # Sort chronologically
        result.sort(key=lambda x: x["date"])
        return result

    def get_timeline_duration(self, timeline_id: str) -> Dict[str, Any]:
        """Calculates total duration from first to last event."""
        first = self.db.query(func.min(ThreatTimelineEvent.timestamp)).filter_by(timeline_id=timeline_id).scalar()
        last = self.db.query(func.max(ThreatTimelineEvent.timestamp)).filter_by(timeline_id=timeline_id).scalar()
        
        if first and last:
            duration = last - first
            return {
                "start": first,
                "end": last,
                "duration_days": duration.days,
                "duration_seconds": duration.total_seconds()
            }
        return {}
