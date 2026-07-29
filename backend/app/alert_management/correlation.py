import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.alert_management import Alert, AlertCorrelationGroup, AlertEvidence

class AlertCorrelationEngine:
    """
    Correlates alerts into groups based on shared IOCs, infrastructure, or threat actors.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def correlate_alert(self, alert_id: uuid.UUID) -> None:
        """
        Background task to correlate an alert.
        Currently implements a basic IOC matching logic.
        """
        # Fetch the alert and its evidence
        result = await self.db.execute(
            select(Alert).where(Alert.id == alert_id)
        )
        alert = result.scalar_one_or_none()
        
        if not alert:
            return

        evidence_result = await self.db.execute(
            select(AlertEvidence).where(AlertEvidence.alert_id == alert_id)
        )
        evidence = evidence_result.scalars().all()
        
        if not evidence:
            return
            
        # Extract values to match against other alerts
        evidence_values = [ev.value for ev in evidence]
        
        # Find other alerts in the same tenant with the same evidence values
        # This is a naive O(N) lookup for MVP, in production this uses the Knowledge Graph
        matching_alerts_query = select(Alert).join(AlertEvidence).where(
            Alert.tenant_id == alert.tenant_id,
            Alert.id != alert.id,
            AlertEvidence.value.in_(evidence_values)
        )
        matching_results = await self.db.execute(matching_alerts_query)
        matching_alerts = matching_results.scalars().all()
        
        if not matching_alerts:
            return
            
        # Group them
        # Check if any matching alert already belongs to a correlation group
        existing_groups = [a.correlation_group_id for a in matching_alerts if a.correlation_group_id]
        
        if existing_groups:
            # Join the first group we found
            target_group_id = existing_groups[0]
            alert.correlation_group_id = target_group_id
        else:
            # Create a new correlation group
            group = AlertCorrelationGroup(
                tenant_id=alert.tenant_id,
                name=f"Correlated Alert Group - {alert.title}",
                correlation_reason="SHARED_IOC"
            )
            self.db.add(group)
            await self.db.flush()
            
            # Add all matched to this group
            for ma in matching_alerts:
                ma.correlation_group_id = group.id
            alert.correlation_group_id = group.id
            
        await self.db.commit()
