import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.ai_triage import AssetBusinessContext

class BusinessImpactEngine:
    """
    Calculates the potential operational and financial impact of an alert 
    by mapping it to the underlying asset's business context.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_impact(self, asset_identifier: str, tenant_id: uuid.UUID) -> float:
        """
        Returns a business impact score between 0 and 100 based on asset criticality and data sensitivity.
        """
        result = await self.db.execute(
            select(AssetBusinessContext).where(
                AssetBusinessContext.asset_identifier == asset_identifier,
                AssetBusinessContext.tenant_id == tenant_id
            )
        )
        asset = result.scalar_one_or_none()
        
        if not asset:
            # Default fallback if asset unknown
            return 30.0
            
        # Base on criticality (1-10) * 10
        score = asset.criticality_score * 10.0
        
        # Bump score based on data sensitivity
        if asset.data_sensitivity == "CONFIDENTIAL":
            score += 20.0
        elif asset.data_sensitivity == "RESTRICTED":
            score += 10.0
            
        return min(score, 100.0)
