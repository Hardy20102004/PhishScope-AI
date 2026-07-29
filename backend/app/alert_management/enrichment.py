import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.alert_management import Alert

class AlertEnrichmentEngine:
    """
    Triggers AI Brain and Threat Intelligence feeds to enrich an alert's context.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def enrich_alert(self, alert_id: uuid.UUID) -> None:
        """
        Background task to enrich an alert.
        """
        result = await self.db.execute(
            select(Alert).where(Alert.id == alert_id)
        )
        alert = result.scalar_one_or_none()
        
        if not alert:
            return
            
        # Mock AI Enrichment
        # In a real implementation, this would call the multi-agent AI brain
        if not alert.ai_summary:
            alert.ai_summary = f"AI Analysis: This alert from {alert.source} requires immediate investigation based on historical patterns. Recommended action: Isolate host."
            
        # Mock Threat Intelligence Enrichment
        if not alert.mitre_techniques:
            # Map category to a mock MITRE technique
            if alert.category.lower() == "malware":
                alert.mitre_techniques = {"T1059": "Command and Scripting Interpreter"}
            elif alert.category.lower() == "phishing":
                alert.mitre_techniques = {"T1566": "Phishing"}
            else:
                alert.mitre_techniques = {"T1078": "Valid Accounts"}
                
        await self.db.commit()
