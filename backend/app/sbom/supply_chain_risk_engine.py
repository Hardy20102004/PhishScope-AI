import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sbom import SupplyChainRiskScore
from app.schemas.sbom import SupplyChainRiskScoreCreate

class SupplyChainRiskEngine:
    """
    Correlates Threat Intel (vulnerabilities) with dependencies to compute risk scores.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_risk(self, tenant_id: uuid.UUID, risk_in: SupplyChainRiskScoreCreate) -> SupplyChainRiskScore:
        # In a real system, this engine would pull vulnerability data, license info,
        # and provenance status to calculate a dynamic score.
        
        score = SupplyChainRiskScore(
            tenant_id=tenant_id,
            sbom_id=risk_in.sbom_id,
            overall_score=risk_in.overall_score,
            vulnerability_risk=risk_in.vulnerability_risk,
            license_risk=risk_in.license_risk,
            provenance_risk=risk_in.provenance_risk
        )
        self.db.add(score)
        await self.db.commit()
        await self.db.refresh(score)
        return score

    async def get_risk_score(self, sbom_id: uuid.UUID) -> Optional[SupplyChainRiskScore]:
        stmt = select(SupplyChainRiskScore).where(SupplyChainRiskScore.sbom_id == sbom_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
