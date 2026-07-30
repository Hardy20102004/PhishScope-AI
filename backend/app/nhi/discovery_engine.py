import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.nhi import NHIMachineIdentity

class DiscoveryEngine:
    """
    Scans and discovers machine identities across cloud (AWS IAM, Entra ID) and k8s environments.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_identities(self, tenant_id: uuid.UUID) -> List[NHIMachineIdentity]:
        result = await self.db.execute(select(NHIMachineIdentity).where(NHIMachineIdentity.tenant_id == tenant_id))
        return result.scalars().all()
