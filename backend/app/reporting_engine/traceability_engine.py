import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.reporting_engine import ReportSection, EvidenceItem

class TraceabilityEngine:
    """
    Ensures that every claim in a report is linked to immutable evidence.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def link_evidence(self, section_id: uuid.UUID, evidence_ids: list[str]) -> ReportSection:
        # Fetch the section
        result = await self.db.execute(select(ReportSection).where(ReportSection.id == section_id))
        section = result.scalar_one_or_none()
        if not section:
            raise ValueError("Section not found")
            
        # Update the traceability links
        section.linked_evidence_ids = list(set(section.linked_evidence_ids + evidence_ids))
        
        await self.db.commit()
        return section
