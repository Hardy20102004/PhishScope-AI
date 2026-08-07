from typing import Any, Dict, Optional
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.alert_management import Alert

class AlertDeduplicationEngine:
    """
    Identifies and handles duplicate or highly similar alerts within a given timeframe.
    Reduces alert fatigue by grouping noisy alerts together.
    """
    
    @staticmethod
    async def find_duplicate(
        db: AsyncSession,
        tenant_id: uuid.UUID,
        source: str,
        source_alert_id: str,
        title: str,
        time_window_minutes: int = 60
    ) -> Optional[Alert]:
        """
        Checks if a similar alert from the same source was recently ingested.
        Matches by source_alert_id (exact) or by source + title within the time window.
        """
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=time_window_minutes)
        
        # 1. Exact match by source_alert_id
        if source_alert_id:
            query = select(Alert).where(
                and_(
                    Alert.tenant_id == tenant_id,
                    Alert.source == source,
                    Alert.source_alert_id == source_alert_id,
                    Alert.created_at >= cutoff_time
                )
            ).order_by(Alert.created_at.desc()).limit(1)
            
            result = await db.execute(query)
            duplicate = result.scalar_one_or_none()
            if duplicate:
                return duplicate
                
        # 2. Similarity match by title and source
        query = select(Alert).where(
            and_(
                Alert.tenant_id == tenant_id,
                Alert.source == source,
                Alert.title == title,
                Alert.created_at >= cutoff_time
            )
        ).order_by(Alert.created_at.desc()).limit(1)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
