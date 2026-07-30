import uuid
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.itdr import ITDRTelemetryEvent

class IdentityTelemetryEngine:
    """
    Collects and normalizes authentication and authorization events.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_telemetry(self, tenant_id: uuid.UUID, event_data: Dict[str, Any]) -> ITDRTelemetryEvent:
        event = ITDRTelemetryEvent(
            tenant_id=tenant_id,
            identity_id=event_data["identity_id"],
            event_type=event_data["event_type"],
            source_ip=event_data.get("source_ip"),
            location=event_data.get("location"),
            device_id=event_data.get("device_id"),
            app_name=event_data.get("app_name"),
            status=event_data["status"],
            metadata_json=event_data.get("metadata_json", {})
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_recent_telemetry(self, tenant_id: uuid.UUID, limit: int = 100) -> List[ITDRTelemetryEvent]:
        result = await self.db.execute(
            select(ITDRTelemetryEvent)
            .where(ITDRTelemetryEvent.tenant_id == tenant_id)
            .order_by(ITDRTelemetryEvent.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()
