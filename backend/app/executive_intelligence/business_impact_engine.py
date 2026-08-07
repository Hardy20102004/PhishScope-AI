import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.executive_intelligence import BusinessImpactIndicator

class BusinessImpactEngine:
    """
    Translates technical risks into business language.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assess_service_impact(self, tenant_id: uuid.UUID, service_name: str, criticality: str, risk_score: float, status: str) -> BusinessImpactIndicator:
        indicator = BusinessImpactIndicator(
            tenant_id=tenant_id,
            service_name=service_name,
            criticality=criticality,
            current_risk_score=risk_score,
            availability_status=status
        )
        self.db.add(indicator)
        await self.db.commit()
        await self.db.refresh(indicator)
        return indicator
