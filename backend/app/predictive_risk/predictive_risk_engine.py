import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.predictive_risk import RiskForecast

class PredictiveRiskEngine:
    """
    Evaluates current posture and generates enterprise risk forecasts.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_forecasts(self, tenant_id: uuid.UUID) -> List[RiskForecast]:
        result = await self.db.execute(select(RiskForecast).where(RiskForecast.tenant_id == tenant_id))
        return result.scalars().all()
