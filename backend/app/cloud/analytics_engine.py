from sqlalchemy.orm import Session
from app.cloud.models import CloudAnalytics, SharedIntelligenceObject, FederationSyncRecord
from sqlalchemy import func
from loguru import logger
import uuid
from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone

class AnalyticsEngine:
    """
    Generates statistics and trends for the Enterprise Cloud.
    """
    def __init__(self, db: Session):
        self.db = db

    def generate_sharing_volume_metric(self):
        """
        Calculates the number of objects shared in the last 24 hours.
        """
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        count = self.db.query(func.count(SharedIntelligenceObject.id)).filter(
            SharedIntelligenceObject.shared_at >= yesterday
        ).scalar()
        
        metric = CloudAnalytics(
            metric_name="sharing_volume_24h",
            metric_value=float(count),
            dimensions={}
        )
        self.db.add(metric)
        self.db.commit()
        logger.info(f"Generated sharing_volume_24h: {count}")
        return metric

    def get_latest_metrics(self, limit: int = 10) -> List[CloudAnalytics]:
        return self.db.query(CloudAnalytics).order_by(CloudAnalytics.timestamp.desc()).limit(limit).all()
