import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.alert_management import AlertAssignment, Alert
from app.models.user import User

class AlertAssignmentEngine:
    """
    Manages the assignment of alerts to analysts, balancing workloads and
    handling escalations.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assign_alert(
        self, 
        alert_id: uuid.UUID, 
        user_id: uuid.UUID, 
        assigned_by: Optional[uuid.UUID] = None
    ) -> AlertAssignment:
        """
        Assigns an alert to a specific user.
        """
        # Deactivate current active assignments
        active_assignments = await self.db.execute(
            select(AlertAssignment).where(
                and_(
                    AlertAssignment.alert_id == alert_id,
                    AlertAssignment.active == True
                )
            )
        )
        for assignment in active_assignments.scalars().all():
            assignment.active = False
            
        # Create new assignment
        new_assignment = AlertAssignment(
            alert_id=alert_id,
            user_id=user_id,
            assigned_by=assigned_by,
            active=True
        )
        self.db.add(new_assignment)
        
        # Update alert status if it was NEW
        alert_result = await self.db.execute(select(Alert).where(Alert.id == alert_id))
        alert = alert_result.scalar_one_or_none()
        if alert and alert.status == "NEW":
            alert.status = "ASSIGNED"
            
        await self.db.commit()
        await self.db.refresh(new_assignment)
        return new_assignment
        
    async def get_analyst_workload(self, tenant_id: uuid.UUID) -> List[dict]:
        """
        Returns the number of active alerts assigned per user in the tenant.
        """
        # A simple approximation for now; in production this uses aggregations
        query = select(AlertAssignment).join(Alert).where(
            and_(
                Alert.tenant_id == tenant_id,
                AlertAssignment.active == True,
                Alert.status.in_(["ASSIGNED", "IN_INVESTIGATION"])
            )
        )
        result = await self.db.execute(query)
        assignments = result.scalars().all()
        
        workload = {}
        for a in assignments:
            workload[a.user_id] = workload.get(a.user_id, 0) + 1
            
        return [{"user_id": uid, "active_cases": count} for uid, count in workload.items()]
