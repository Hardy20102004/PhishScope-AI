import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cwpp import RuntimeEvent, BehaviorAnomaly

class BehaviorAnalyticsEngine:
    """
    Analyzes runtime events against behavioral baselines to detect anomalies.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_event(self, event: RuntimeEvent) -> BehaviorAnomaly:
        """
        Simple anomaly detection logic for MVP.
        Flags unexpected interactive shells or crypto-mining indicators.
        """
        if event.event_type == "PROCESS_START" and event.process_name in ["nc", "bash", "sh"] and "-e" in (event.command_line or ""):
            anomaly = BehaviorAnomaly(
                tenant_id=event.tenant_id,
                workload_id=event.workload_id,
                event_id=event.id,
                title="Interactive Reverse Shell Detected",
                severity="CRITICAL",
                description=f"Process {event.process_name} executed with arguments indicating a reverse shell: {event.command_line}"
            )
            self.db.add(anomaly)
            await self.db.commit()
            await self.db.refresh(anomaly)
            return anomaly
        return None
