import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.multi_cloud import UnifiedCloudAsset

class UnifiedAssetEngine:
    """
    Aggregates data from CSPM, CWPP, CIEM, K8s, and DSPM into a single inventory.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_asset(
        self, 
        tenant_id: uuid.UUID, 
        name: str, 
        provider: str, 
        asset_type: str, 
        environment: str,
        native_id: str
    ) -> UnifiedCloudAsset:
        asset = UnifiedCloudAsset(
            tenant_id=tenant_id,
            asset_name=name,
            provider=provider,
            asset_type=asset_type,
            environment=environment,
            native_id=native_id
        )
        self.db.add(asset)
        await self.db.commit()
        await self.db.refresh(asset)
        return asset
