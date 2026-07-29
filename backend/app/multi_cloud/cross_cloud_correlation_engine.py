import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.multi_cloud import CrossCloudRelationship, UnifiedCloudAsset

class CrossCloudCorrelationEngine:
    """
    Builds the graph of relationships between disparate cloud assets.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def link_assets(self, tenant_id: uuid.UUID, source: UnifiedCloudAsset, target: UnifiedCloudAsset, rel_type: str) -> CrossCloudRelationship:
        link = CrossCloudRelationship(
            tenant_id=tenant_id,
            source_asset_id=source.id,
            target_asset_id=target.id,
            relationship_type=rel_type
        )
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link
