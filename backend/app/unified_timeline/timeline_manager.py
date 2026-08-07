import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.unified_timeline import UnifiedInvestigation, UnifiedTimelineEvent

class TimelineManager:
    """
    Handles ingestion and normalization of artifacts from disparate modules into a single timeline.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_unified_session(self, tenant_id: uuid.UUID, name: str, inv_id: uuid.UUID = None) -> UnifiedInvestigation:
        session = UnifiedInvestigation(
            tenant_id=tenant_id,
            investigation_id=inv_id,
            name=name
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def import_mock_events(self, session_id: uuid.UUID) -> list[UnifiedTimelineEvent]:
        now = datetime.now(timezone.utc)
        
        events = [
            # 1. Initial Phishing Email
            UnifiedTimelineEvent(
                inv_id=session_id,
                timestamp=now - timedelta(days=2),
                source_module="EMAIL",
                source_table="mf_email_messages",
                source_id="msg_123",
                event_type="EMAIL_DELIVERY",
                event_summary="Phishing email 'Invoice Update' delivered to ceo@company.com",
                render_metadata={"sender": "billing@evil.com", "attachment": "invoice.exe"}
            ),
            # 2. User clicks and drops payload on Disk
            UnifiedTimelineEvent(
                inv_id=session_id,
                timestamp=now - timedelta(days=2, minutes=-5),
                source_module="DISK",
                source_table="mf_file_system_entries",
                source_id="fs_456",
                event_type="FILE_CREATION",
                event_summary="invoice.exe written to C:\\Users\\ceo\\Downloads",
                render_metadata={"path": "C:\\Users\\ceo\\Downloads\\invoice.exe", "hash": "3a20e8b2..."}
            ),
            # 3. Payload executes and beacons out (Memory/Network)
            UnifiedTimelineEvent(
                inv_id=session_id,
                timestamp=now - timedelta(days=2, minutes=-6),
                source_module="MEMORY",
                source_table="mf_network_connections",
                source_id="net_789",
                event_type="NETWORK_CONNECTION",
                event_summary="invoice.exe initiated outbound connection to 203.0.113.5",
                render_metadata={"process": "invoice.exe", "dest_ip": "203.0.113.5", "port": 443}
            ),
            # 4. Attacker uses stolen creds to pivot to cloud
            UnifiedTimelineEvent(
                inv_id=session_id,
                timestamp=now - timedelta(days=1),
                source_module="CLOUD",
                source_table="mf_cloud_audit_logs",
                source_id="cloud_001",
                event_type="IAM_ASSUME_ROLE",
                event_summary="Role assumed from external malicious IP",
                render_metadata={"actor": "ceo-role", "source_ip": "203.0.113.5"}
            )
        ]
        
        for e in events:
            self.db.add(e)
            
        await self.db.commit()
        return events
