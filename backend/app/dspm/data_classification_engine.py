import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dspm import DataClassification, CloudDataAsset

class DataClassificationEngine:
    """
    Assigns sensitivity labels based on content patterns/metadata.
    Supports future AI/LLM integration.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def classify_asset(self, asset: CloudDataAsset, label: str, confidence: float) -> DataClassification:
        classification = DataClassification(
            tenant_id=asset.tenant_id,
            asset_id=asset.id,
            label=label,
            confidence_score=confidence,
            requires_review=confidence < 0.8
        )
        self.db.add(classification)
        await self.db.commit()
        await self.db.refresh(classification)
        return classification
