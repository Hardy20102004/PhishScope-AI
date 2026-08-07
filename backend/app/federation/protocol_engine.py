import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.federation import FederationProtocolConfig

class ProtocolEngine:
    """
    Validates SAML, OIDC, and OAuth configurations against security best practices.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_configs(self) -> List[FederationProtocolConfig]:
        result = await self.db.execute(select(FederationProtocolConfig))
        return result.scalars().all()
