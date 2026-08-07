import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.identity_intel import IdentityTelemetry

class CorrelationEngine:
    """
    Correlates identity telemetry from across the enterprise (SSO, PAM, IGA, Workloads).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_telemetry(self, tenant_id: uuid.UUID) -> List[IdentityTelemetry]:
        result = await self.db.execute(select(IdentityTelemetry).where(IdentityTelemetry.tenant_id == tenant_id))
        return result.scalars().all()
