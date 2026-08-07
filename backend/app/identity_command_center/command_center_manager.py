import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.identity_command_center import EnterpriseIdentityPortfolio, IdentityHealthMetric

class CommandCenterManager:
    """
    Orchestrates the retrieval of data from all identity modules to provide a unified portfolio.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_portfolio(self, tenant_id: uuid.UUID) -> List[EnterpriseIdentityPortfolio]:
        result = await self.db.execute(select(EnterpriseIdentityPortfolio).where(EnterpriseIdentityPortfolio.tenant_id == tenant_id))
        return result.scalars().all()

    async def get_health_metrics(self, tenant_id: uuid.UUID) -> List[IdentityHealthMetric]:
        result = await self.db.execute(select(IdentityHealthMetric).where(IdentityHealthMetric.tenant_id == tenant_id).order_by(IdentityHealthMetric.measured_at.desc()).limit(1))
        return result.scalars().all()
