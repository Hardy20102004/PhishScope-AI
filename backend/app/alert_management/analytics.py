import uuid
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text

from app.models.alert_management import Alert, AlertLifecycleEvent

class AlertAnalyticsEngine:
    """
    Generates SOC metrics, alert volume trends, and analyst performance data.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_metrics(self, tenant_id: uuid.UUID) -> Dict[str, Any]:
        """
        Calculates high-level metrics for the SOC Dashboard.
        Includes volume, open alerts, priority breakdown.
        """
        # Total active alerts
        active_query = select(func.count(Alert.id)).where(
            Alert.tenant_id == tenant_id,
            Alert.status.notin_(["RESOLVED", "CLOSED"])
        )
        active_count = await self.db.execute(active_query)
        active_alerts = active_count.scalar() or 0

        # High priority active alerts
        critical_query = select(func.count(Alert.id)).where(
            Alert.tenant_id == tenant_id,
            Alert.status.notin_(["RESOLVED", "CLOSED"]),
            Alert.severity.in_(["HIGH", "CRITICAL"])
        )
        critical_count = await self.db.execute(critical_query)
        critical_alerts = critical_count.scalar() or 0
        
        # Priority Distribution
        dist_query = select(Alert.severity, func.count(Alert.id)).where(
            Alert.tenant_id == tenant_id
        ).group_by(Alert.severity)
        dist_result = await self.db.execute(dist_query)
        
        distribution = {row[0]: row[1] for row in dist_result.all()}
        
        # Source Distribution
        source_query = select(Alert.source, func.count(Alert.id)).where(
            Alert.tenant_id == tenant_id
        ).group_by(Alert.source)
        source_result = await self.db.execute(source_query)
        
        sources = {row[0]: row[1] for row in source_result.all()}

        return {
            "active_alerts": active_alerts,
            "critical_alerts": critical_alerts,
            "priority_distribution": distribution,
            "source_distribution": sources,
            "mtta_minutes": 15, # Mock value for now, requires complex time diff logic
            "mttr_minutes": 120 # Mock value
        }
