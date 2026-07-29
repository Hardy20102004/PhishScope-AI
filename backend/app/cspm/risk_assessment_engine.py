import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cspm import CSPMCloudAsset, CloudMisconfiguration

class RiskAssessmentEngine:
    """
    Evaluates configurations to identify specific security risks.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def evaluate_asset_risk(self, asset: CSPMCloudAsset) -> CloudMisconfiguration:
        """
        Simple evaluation logic for MVP.
        Checks configuration dict for known bad states.
        """
        severity = "LOW"
        title = "Best Practice Violation"
        
        config = asset.configuration
        if config.get("publicly_accessible", False) and not config.get("encrypted", True):
            severity = "CRITICAL"
            title = "Unencrypted Public Resource"
        elif config.get("publicly_accessible", False):
            severity = "HIGH"
            title = "Publicly Accessible Resource"
        elif not config.get("encrypted", True):
            severity = "MEDIUM"
            title = "Unencrypted Resource"
            
        misc = CloudMisconfiguration(
            tenant_id=asset.tenant_id,
            asset_id=asset.id,
            title=title,
            severity=severity,
            description=f"Risk identified on {asset.asset_name}",
            remediation_steps="Apply internal security baseline."
        )
        self.db.add(misc)
        await self.db.commit()
        await self.db.refresh(misc)
        return misc
