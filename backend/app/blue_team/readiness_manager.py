import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.blue_team.maturity_engine import MaturityEngine

class ReadinessManager:
    """
    Orchestrates the calculation and retrieval of overall Blue Team readiness.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_current_readiness(self, tenant_id: uuid.UUID):
        # Delegate to the Maturity Engine to synthesize the latest metrics
        engine = MaturityEngine(self.db)
        snapshot = await engine.calculate_maturity_score(tenant_id)
        return snapshot
