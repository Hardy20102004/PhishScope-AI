import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.alert_management import AlertLifecycleEvent

class AlertAuditService:
    """
    Provides audit trails for alerts, tracking state changes, assignments, and analyst comments
    to maintain compliance and a chronological timeline of an investigation.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_event(
        self,
        alert_id: uuid.UUID,
        new_status: str,
        previous_status: Optional[str] = None,
        user_id: Optional[uuid.UUID] = None,
        comment: Optional[str] = None
    ) -> AlertLifecycleEvent:
        """
        Logs a lifecycle event for an alert.
        """
        event = AlertLifecycleEvent(
            alert_id=alert_id,
            new_status=new_status,
            previous_status=previous_status,
            user_id=user_id,
            comment=comment
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event
        
    async def get_audit_trail(self, alert_id: uuid.UUID) -> List[AlertLifecycleEvent]:
        """
        Retrieves the chronological audit trail for a specific alert.
        """
        query = select(AlertLifecycleEvent).where(
            AlertLifecycleEvent.alert_id == alert_id
        ).order_by(AlertLifecycleEvent.changed_at.asc())
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
