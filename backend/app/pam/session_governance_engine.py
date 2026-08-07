import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.pam import PAMSessionRecord

class SessionGovernanceEngine:
    """
    Monitors active administrative sessions.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_sessions(self, tenant_id: uuid.UUID) -> List[PAMSessionRecord]:
        result = await self.db.execute(select(PAMSessionRecord).where(PAMSessionRecord.tenant_id == tenant_id))
        return result.scalars().all()
