import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ciem import CloudEntitlement

class EntitlementAnalysisEngine:
    """
    Calculates the flattened effective permissions matrix for identities.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_entitlement(
        self, 
        tenant_id: uuid.UUID, 
        identity_id: uuid.UUID, 
        res_type: str, 
        action: str, 
        is_admin: bool
    ) -> CloudEntitlement:
        entitlement = CloudEntitlement(
            tenant_id=tenant_id,
            identity_id=identity_id,
            resource_type=res_type,
            action=action,
            is_admin_privilege=is_admin
        )
        self.db.add(entitlement)
        await self.db.commit()
        await self.db.refresh(entitlement)
        return entitlement
