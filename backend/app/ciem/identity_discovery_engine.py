import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ciem import CIEMCloudIdentity

class IdentityDiscoveryEngine:
    """
    Inventories identities across AWS, Azure, GCP.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_identity(
        self, 
        tenant_id: uuid.UUID, 
        name: str, 
        type: str, 
        provider: str, 
        account_id: str,
        mfa: bool = False,
        last_login: datetime = None
    ) -> CIEMCloudIdentity:
        identity = CIEMCloudIdentity(
            tenant_id=tenant_id,
            identity_name=name,
            identity_type=type,
            provider=provider,
            account_id=account_id,
            mfa_enabled=mfa,
            last_login=last_login
        )
        self.db.add(identity)
        await self.db.commit()
        await self.db.refresh(identity)
        return identity
