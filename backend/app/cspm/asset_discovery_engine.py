import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cspm import CSPMCloudAsset
from typing import Dict, Any

class CSPMCloudAssetDiscoveryEngine:
    """
    Simulates the ingestion and normalization of multi-cloud asset inventories.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_asset(self, tenant_id: uuid.UUID, provider: str, a_type: str, name: str, region: str, config: Dict[str, Any]) -> CSPMCloudAsset:
        asset = CSPMCloudAsset(
            tenant_id=tenant_id,
            provider=provider,
            asset_type=a_type,
            asset_name=name,
            region=region,
            configuration=config
        )
        self.db.add(asset)
        await self.db.commit()
        await self.db.refresh(asset)
        return asset
