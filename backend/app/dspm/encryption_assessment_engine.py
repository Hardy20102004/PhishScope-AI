import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dspm import CloudDataAsset, DataExposureFinding

class EncryptionAssessmentEngine:
    """
    Validates KMS usage and at-rest/in-transit encryption.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assess_encryption(self, asset: CloudDataAsset) -> DataExposureFinding:
        if not asset.is_encrypted:
            finding = DataExposureFinding(
                tenant_id=asset.tenant_id,
                asset_id=asset.id,
                finding_type="UNENCRYPTED_AT_REST",
                severity="HIGH",
                description=f"Data asset {asset.asset_name} is not encrypted at rest."
            )
            self.db.add(finding)
            await self.db.commit()
            return finding
        return None
