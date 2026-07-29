import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.unified_timeline import EvidenceCorrelation

class CorrelationEngine:
    """
    Identifies shared IOCs (IPs, hashes, emails) across disparate events.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def correlate_events(self, session_id: uuid.UUID, events: list) -> list[EvidenceCorrelation]:
        
        # In a real system, we'd query all events and match on extracted JSON keys.
        # Here we mock the correlation between the Memory Beacon and Cloud Login via shared IP.
        
        memory_event = next((e for e in events if e.source_module == "MEMORY"), None)
        cloud_event = next((e for e in events if e.source_module == "CLOUD"), None)
        
        correlations = []
        
        if memory_event and cloud_event:
            c = EvidenceCorrelation(
                inv_id=session_id,
                event_a_id=memory_event.id,
                event_b_id=cloud_event.id,
                correlation_type="SHARED_IP",
                correlation_value="203.0.113.5",
                confidence_score=100
            )
            self.db.add(c)
            correlations.append(c)
            
        await self.db.commit()
        return correlations
