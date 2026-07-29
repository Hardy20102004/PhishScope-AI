import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cloud_forensics import CloudAuditLog

class AuditEngine:
    """
    Simulates parsing AWS CloudTrail / GCP Audit logs to detect identity compromises.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_logs(self, env_id: uuid.UUID) -> list[CloudAuditLog]:
        now = datetime.now(timezone.utc)
        
        # Mocking CloudTrail Events
        logs = [
            CloudAuditLog(
                env_id=env_id,
                event_name="AssumeRole",
                event_source="sts.amazonaws.com",
                actor_identity="arn:aws:iam::123456789012:user/developer-01",
                source_ip="203.0.113.5",
                is_anomalous=False,
                raw_event={"requestParameters": {"roleArn": "arn:aws:iam::123456789012:role/AdminRole"}},
                timestamp=now - timedelta(hours=2)
            ),
            CloudAuditLog(
                env_id=env_id,
                event_name="CreateAccessKey",
                event_source="iam.amazonaws.com",
                actor_identity="arn:aws:sts::123456789012:assumed-role/AdminRole/developer-01",
                source_ip="203.0.113.5", # External IP (Anomalous)
                is_anomalous=True,
                anomaly_reason="Long-term credential creation by assumed role from untrusted IP.",
                raw_event={"requestParameters": {"userName": "developer-01"}},
                timestamp=now - timedelta(hours=1, minutes=55)
            )
        ]
        
        for log in logs:
            self.db.add(log)
            
        await self.db.commit()
        return logs
