import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.identity_command_center import ExecutiveDecisionLog

class ExecutiveDecisionEngine:
    """
    Generates strategic recommendations and tracks human-approved governance decisions.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_decision_logs(self, tenant_id: uuid.UUID) -> List[ExecutiveDecisionLog]:
        result = await self.db.execute(select(ExecutiveDecisionLog).where(ExecutiveDecisionLog.tenant_id == tenant_id))
        return result.scalars().all()
