import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sast import SASTFinding, FindingSeverity

class RiskPrioritizationEngine:
    """
    Dynamically scores the severity of findings based on business context and exploitability estimates.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def prioritize_finding(self, finding_id: uuid.UUID) -> SASTFinding:
        # In a real system, this engine would look at code exposure (is this file public-facing?)
        # and adjust the exploitability score and severity dynamically.
        stmt = select(SASTFinding).where(SASTFinding.id == finding_id)
        finding = (await self.db.execute(stmt)).scalar_one_or_none()
        
        if finding:
            # Example adjustment
            finding.exploitability_score += 1.0
            if finding.exploitability_score >= 8.0:
                finding.severity = FindingSeverity.CRITICAL
                
            await self.db.commit()
            await self.db.refresh(finding)
            
        return finding
