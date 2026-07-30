from typing import Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.zta import ZTAContextSnapshot

class ContextEvaluationEngine:
    """
    Aggregates and normalizes context signals.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def capture_snapshot(self, tenant_id: uuid.UUID, raw_context: Dict[str, Any]) -> ZTAContextSnapshot:
        """
        Creates a point-in-time snapshot of context.
        """
        snapshot = ZTAContextSnapshot(
            tenant_id=tenant_id,
            identity_id=raw_context.get("identity_id"),
            device_id=raw_context.get("device_id"),
            session_id=raw_context.get("session_id"),
            application_id=raw_context.get("application_id"),
            identity_context=raw_context.get("identity_context", {}),
            device_context=raw_context.get("device_context", {}),
            network_context=raw_context.get("network_context", {}),
            location_context=raw_context.get("location_context", {}),
            auth_context=raw_context.get("auth_context", {})
        )
        self.db.add(snapshot)
        await self.db.commit()
        await self.db.refresh(snapshot)
        return snapshot
