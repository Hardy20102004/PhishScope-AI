import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.digital_twin import AttackPathGraph

class AttackPathEngine:
    """
    Analyzes relationships and trust chains to discover potential attack paths.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_attack_paths(self, tenant_id: uuid.UUID) -> List[AttackPathGraph]:
        result = await self.db.execute(select(AttackPathGraph).where(AttackPathGraph.tenant_id == tenant_id))
        return result.scalars().all()
