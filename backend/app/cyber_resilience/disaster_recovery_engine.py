import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cyber_resilience import DisasterRecoveryTest

class DisasterRecoveryEngine:
    """
    Assesses backup readiness, infrastructure recovery procedures, and tracks historical DR tests.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dr_tests(self, tenant_id: uuid.UUID) -> List[DisasterRecoveryTest]:
        result = await self.db.execute(select(DisasterRecoveryTest).where(DisasterRecoveryTest.tenant_id == tenant_id))
        return result.scalars().all()
