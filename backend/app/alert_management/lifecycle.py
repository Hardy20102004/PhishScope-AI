import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.alert_management import Alert, AlertLifecycleEvent

class AlertLifecycleManager:
    """
    Manages the state transitions of an alert and logs audit events.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_status(self, alert_id: uuid.UUID, new_status: str, user_id: Optional[uuid.UUID] = None, comment: Optional[str] = None) -> Alert:
        """
        Updates the alert status and records a lifecycle event.
        Valid statuses: NEW, ASSIGNED, IN_INVESTIGATION, ESCALATED, RESOLVED, CLOSED
        """
        result = await self.db.execute(
            select(Alert).where(Alert.id == alert_id)
        )
        alert = result.scalar_one_or_none()
        
        if not alert:
            raise ValueError(f"Alert with id {alert_id} not found")
            
        previous_status = alert.status
        if previous_status == new_status:
            return alert # No change
            
        alert.status = new_status
        
        lifecycle_event = AlertLifecycleEvent(
            alert_id=alert.id,
            user_id=user_id,
            previous_status=previous_status,
            new_status=new_status,
            comment=comment
        )
        
        self.db.add(lifecycle_event)
        await self.db.commit()
        await self.db.refresh(alert)
        
        return alert
