import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ctem import AttackSurfaceNode

class AttackSurfaceEngine:
    """
    Queries the multi-cloud inventory specifically for internet-facing assets and exposed APIs.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_exposed_node(self, tenant_id: uuid.UUID, asset_id: str, asset_type: str, vector: str) -> AttackSurfaceNode:
        node = AttackSurfaceNode(
            tenant_id=tenant_id,
            asset_id=asset_id,
            asset_type=asset_type,
            exposure_vector=vector,
            is_active=True
        )
        self.db.add(node)
        await self.db.commit()
        await self.db.refresh(node)
        return node
