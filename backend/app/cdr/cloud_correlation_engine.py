import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cdr import CloudDetection, CloudInvestigation, CloudTelemetryEvent
from sqlalchemy import select

class CloudCorrelationEngine:
    """
    Groups isolated detections into broader CloudInvestigation cases based on entity overlap.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def correlate_detection(self, detection: CloudDetection, event: CloudTelemetryEvent) -> CloudInvestigation:
        # Simple entity-graph correlation: Try to find an open investigation for this principal
        if not event.principal_id:
            return None
            
        res = await self.db.execute(select(CloudInvestigation).where(
            CloudInvestigation.tenant_id == detection.tenant_id,
            CloudInvestigation.status == "OPEN",
            CloudInvestigation.primary_entity == event.principal_id
        ))
        investigation = res.scalars().first()
        
        if not investigation:
            investigation = CloudInvestigation(
                tenant_id=detection.tenant_id,
                title=f"Suspicious Activity: {event.principal_id}",
                primary_entity=event.principal_id
            )
            self.db.add(investigation)
            await self.db.flush() # get ID
            
        # Link detection
        detection.investigation_id = investigation.id
        await self.db.commit()
        await self.db.refresh(investigation)
        return investigation
