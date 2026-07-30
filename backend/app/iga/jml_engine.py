import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.iga import IGALifecycleEvent

class JMLEngine:
    """
    Manages Joiner, Mover, and Leaver lifecycle events.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_event(self, tenant_id: uuid.UUID, data: Dict[str, Any]) -> IGALifecycleEvent:
        event = IGALifecycleEvent(
            tenant_id=tenant_id,
            identity_id=data["identity_id"],
            event_type=data["event_type"],
            source_system=data["source_system"],
            effective_date=data["effective_date"],
            metadata_json=data.get("metadata_json", {})
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_events(self, tenant_id: uuid.UUID, limit: int = 100) -> List[IGALifecycleEvent]:
        result = await self.db.execute(
            select(IGALifecycleEvent)
            .where(IGALifecycleEvent.tenant_id == tenant_id)
            .order_by(IGALifecycleEvent.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
