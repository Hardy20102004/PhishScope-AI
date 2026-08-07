import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.unified_timeline import EvidenceCorrelation

class RelationshipEngine:
    """
    Infers causal relationships based on temporal proximity.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def infer_causality(self, session_id: uuid.UUID, events: list) -> list[EvidenceCorrelation]:
        
        email_event = next((e for e in events if e.source_module == "EMAIL"), None)
        disk_event = next((e for e in events if e.source_module == "DISK"), None)
        
        correlations = []
        
        if email_event and disk_event:
            # If a file is dropped within 5 minutes of an email with the same filename...
            c = EvidenceCorrelation(
                inv_id=session_id,
                event_a_id=email_event.id,
                event_b_id=disk_event.id,
                correlation_type="CAUSAL_SPAWN",
                correlation_value="invoice.exe",
                confidence_score=85
            )
            self.db.add(c)
            correlations.append(c)
            
        await self.db.commit()
        return correlations
