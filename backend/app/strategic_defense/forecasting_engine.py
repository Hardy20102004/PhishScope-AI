import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.strategic_defense import StrategicForecast
from datetime import datetime

class ForecastingEngine:
    """
    Uses historical data to project future risk and operational trends.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_forecast(self, tenant_id: uuid.UUID, metric: str, target: datetime, value: float, confidence: float) -> StrategicForecast:
        forecast = StrategicForecast(
            tenant_id=tenant_id,
            metric_name=metric,
            target_date=target,
            projected_value=value,
            confidence_score=confidence
        )
        self.db.add(forecast)
        await self.db.commit()
        await self.db.refresh(forecast)
        return forecast
