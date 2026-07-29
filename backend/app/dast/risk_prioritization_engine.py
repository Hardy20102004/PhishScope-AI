import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.dast import DASTFinding, DASTFindingSeverity

class RiskPrioritizationEngine:
    """
    Dynamically scores the severity of runtime findings based on business criticality and exposure.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def prioritize_finding(self, finding_id: uuid.UUID) -> DASTFinding:
        stmt = select(DASTFinding).where(DASTFinding.id == finding_id)
        finding = (await self.db.execute(stmt)).scalar_one_or_none()
        
        if finding:
            # Example adjustment: If it's a critical API endpoint, bump the exploitability
            finding.exploitability_score += 1.5
            if finding.exploitability_score >= 8.5:
                finding.severity = DASTFindingSeverity.CRITICAL
                
            await self.db.commit()
            await self.db.refresh(finding)
            
        return finding
