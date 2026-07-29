import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cdr import CDRCloudInvestigation

class CDRRiskEngine:
    """
    Calculates the overall severity and business impact of an incident.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_investigation_priority(self, investigation: CDRCloudInvestigation) -> str:
        # In a real system, this would evaluate the number of linked detections and resource criticality.
        investigation.priority = "HIGH"
        self.db.add(investigation)
        await self.db.commit()
        return "HIGH"
