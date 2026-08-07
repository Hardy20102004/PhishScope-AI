import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cyber_resilience import MaturityAssessment

class MaturityAssessmentEngine:
    """
    Evaluates operational data to assign a maturity tier (1-5) to different security domains.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_domain_maturity(self, tenant_id: uuid.UUID, domain: str, operational_score: float) -> MaturityAssessment:
        # Maps an operational score (0-100) to a CMMI 1-5 tier
        tier = 1 # Initial
        if operational_score >= 85:
            tier = 5 # Optimizing
        elif operational_score >= 70:
            tier = 4 # Quantitatively Managed
        elif operational_score >= 55:
            tier = 3 # Defined
        elif operational_score >= 40:
            tier = 2 # Managed
            
        justification = f"Calculated based on operational index score of {operational_score}."
        
        assessment = MaturityAssessment(
            tenant_id=tenant_id,
            domain=domain,
            maturity_tier=tier,
            justification=justification
        )
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        return assessment
