import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dspm import CloudDataAsset

class DataDiscoveryEngine:
    """
    Inventories cloud storage services.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_asset(
        self, 
        tenant_id: uuid.UUID, 
        name: str, 
        provider: str, 
        service_type: str, 
        location: str,
        is_public: bool = False,
        is_encrypted: bool = False
    ) -> CloudDataAsset:
        asset = CloudDataAsset(
            tenant_id=tenant_id,
            asset_name=name,
            provider=provider,
            service_type=service_type,
            location=location,
            is_public=is_public,
            is_encrypted=is_encrypted
        )
        self.db.add(asset)
        await self.db.commit()
        await self.db.refresh(asset)
        return asset
