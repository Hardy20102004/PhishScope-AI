import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cdr import CloudTelemetryEvent

class TelemetryNormalizationEngine:
    """
    Ingests multi-cloud logs and maps them to a standard schema.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_event(
        self, 
        tenant_id: uuid.UUID, 
        provider: str, 
        source: str, 
        name: str, 
        raw: dict,
        principal_id: str = None,
        resource_id: str = None
    ) -> CloudTelemetryEvent:
        event = CloudTelemetryEvent(
            tenant_id=tenant_id,
            provider=provider,
            event_source=source,
            event_name=name,
            principal_id=principal_id,
            resource_id=resource_id,
            raw_data=raw
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event
