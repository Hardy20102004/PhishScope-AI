import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cdr import CloudTelemetryEvent, CloudDetection

class CloudDetectionEngine:
    """
    Analyzes normalized telemetry against detection rules.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_event(self, event: CloudTelemetryEvent) -> CloudDetection:
        """
        Simple MVP rule: Flag AWS ConsoleLogin without MFA.
        """
        raw = event.raw_data
        if event.event_name == "ConsoleLogin" and raw.get("responseElements", {}).get("ConsoleLogin") == "Success":
            if raw.get("additionalEventData", {}).get("MFAUsed") != "Yes":
                detection = CloudDetection(
                    tenant_id=event.tenant_id,
                    rule_name="AWS Console Login Without MFA",
                    severity="HIGH",
                    description=f"User {event.principal_id} logged into AWS console without MFA.",
                    mitre_tactics=["TA0001", "TA0006"],
                    evidence_events=[str(event.id)]
                )
                self.db.add(detection)
                await self.db.commit()
                await self.db.refresh(detection)
                return detection
        return None
