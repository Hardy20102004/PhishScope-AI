import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cloud_forensics import CloudEnvironment

class EvidenceManager:
    """
    Handles registration of the cloud investigation context.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_environment(self, tenant_id: uuid.UUID, provider: str, account_id: str, region: str, inv_id: uuid.UUID = None) -> CloudEnvironment:
        env = CloudEnvironment(
            tenant_id=tenant_id,
            investigation_id=inv_id,
            provider=provider,
            account_id=account_id,
            region=region
        )
        
        self.db.add(env)
        await self.db.commit()
        await self.db.refresh(env)
        return env
