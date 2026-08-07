import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.executive_intelligence import InvestmentROI

class InvestmentAnalyticsEngine:
    """
    Calculates the operational return on engineering investment.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_investment_roi(self, tenant_id: uuid.UUID, initiative: str, status: str, hours_saved: float, risk_reduction: float) -> InvestmentROI:
        roi = InvestmentROI(
            tenant_id=tenant_id,
            initiative_name=initiative,
            status=status,
            hours_saved_monthly=hours_saved,
            risk_reduction_percentage=risk_reduction
        )
        self.db.add(roi)
        await self.db.commit()
        await self.db.refresh(roi)
        return roi
