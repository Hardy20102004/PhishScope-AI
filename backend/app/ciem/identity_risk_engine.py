import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ciem import IdentityRiskScore, CIEMCloudIdentity
from app.ciem.least_privilege_engine import LeastPrivilegeEngine
from sqlalchemy import select

class IdentityRiskEngine:
    """
    Aggregates excessive permissions and identity hygiene into a risk score.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_risk_score(self, tenant_id: uuid.UUID, identity: CIEMCloudIdentity) -> IdentityRiskScore:
        lpe = LeastPrivilegeEngine(self.db)
        risk_factors = await lpe.evaluate_identity_hygiene(identity)
        
        score = 0.0
        if "Holds Administrative Privilege" in risk_factors:
            score += 40.0
        if "No MFA Configured" in risk_factors:
            score += 30.0
        if "Dormant Identity (>90 Days)" in risk_factors:
            score += 30.0
            
        res = await self.db.execute(select(IdentityRiskScore).where(IdentityRiskScore.identity_id == identity.id))
        risk_record = res.scalars().first()
        
        if not risk_record:
            risk_record = IdentityRiskScore(tenant_id=tenant_id, identity_id=identity.id, risk_score=score, risk_factors=risk_factors)
            self.db.add(risk_record)
        else:
            risk_record.risk_score = score
            risk_record.risk_factors = risk_factors
            
        await self.db.commit()
        await self.db.refresh(risk_record)
        return risk_record
