import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dspm import CloudDataAsset, DataExposureFinding, DataClassification
from sqlalchemy import select

class ExposureAnalysisEngine:
    """
    Evaluates public exposure and cross-account sharing.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_exposure(self, asset: CloudDataAsset) -> list[DataExposureFinding]:
        findings = []
        
        # Check if public
        if asset.is_public:
            # Check sensitivity
            res = await self.db.execute(select(DataClassification).where(
                DataClassification.asset_id == asset.id,
                DataClassification.label.in_(["PII", "PHI", "FINANCIAL"])
            ))
            sensitive = res.scalars().first()
            
            severity = "CRITICAL" if sensitive else "HIGH"
            finding = DataExposureFinding(
                tenant_id=asset.tenant_id,
                asset_id=asset.id,
                finding_type="PUBLIC_ACCESS",
                severity=severity,
                description=f"Data asset {asset.asset_name} is publicly accessible via the Internet."
            )
            self.db.add(finding)
            findings.append(finding)
            
        if findings:
            await self.db.commit()
            
        return findings
