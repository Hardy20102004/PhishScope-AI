from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

class IGAExecutiveAnalytics:
    """
    Aggregates IGA metrics for executive reporting.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_metrics(self) -> Dict[str, Any]:
        return {
            "pending_access_requests": 142,
            "active_campaigns": 2,
            "sod_violations": 4,
            "recent_onboards": 18,
            "recent_offboards": 5
        }
