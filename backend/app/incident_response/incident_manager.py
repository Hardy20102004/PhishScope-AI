import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.incident_response import Incident, DFIRCase

class IncidentManager:
    """
    Manages the overarching incident lifecycle.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_incident(self, title: str, description: str, severity: str, tenant_id: uuid.UUID, user_id: uuid.UUID) -> Incident:
        incident = Incident(
            tenant_id=tenant_id,
            title=title,
            description=description,
            severity=severity,
            status="NEW",
            lead_investigator_id=user_id
        )
        self.db.add(incident)
        await self.db.flush()
        
        # Auto-create a default DFIR Case attached to this incident
        default_case = DFIRCase(
            incident_id=incident.id,
            title=f"Investigation: {title}",
            case_type="FORENSICS"
        )
        self.db.add(default_case)
        await self.db.commit()
        await self.db.refresh(incident)
        
        return incident

    async def update_status(self, incident_id: uuid.UUID, new_status: str) -> Incident:
        """
        Transitions the incident state. E.g., NEW -> INVESTIGATING -> CONTAINMENT -> RESOLVED
        """
        result = await self.db.execute(select(Incident).where(Incident.id == incident_id))
        incident = result.scalar_one_or_none()
        
        if not incident:
            raise ValueError("Incident not found")
            
        incident.status = new_status
        if new_status in ["RESOLVED", "CLOSED"]:
            incident.resolved_at = datetime.now(timezone.utc)
            
        await self.db.commit()
        await self.db.refresh(incident)
        return incident
