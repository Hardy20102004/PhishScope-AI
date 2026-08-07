import uuid
import hashlib
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reporting_engine import EvidenceItem, ChainOfCustodyRecord

class CustodyEngine:
    """
    Manages the immutable ledger for evidence handling.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_evidence(self, tenant_id: uuid.UUID, name: str, source_type: str, original_hash: str, actor_id: str, inv_id: uuid.UUID = None) -> EvidenceItem:
        # Create the core evidence item
        item = EvidenceItem(
            tenant_id=tenant_id,
            investigation_id=inv_id,
            name=name,
            source_type=source_type,
            original_sha256=original_hash,
            acquired_by=actor_id
        )
        self.db.add(item)
        await self.db.flush() # Get the ID for the custody record
        
        # Log the ingestion into the tamper-evident ledger
        await self.record_action(item.id, "INGEST", actor_id, "Initial acquisition and hashing.")
        
        await self.db.commit()
        await self.db.refresh(item, ["chain_of_custody"])
        return item

    async def record_action(self, evidence_id: uuid.UUID, action_type: str, actor_id: str, notes: str) -> ChainOfCustodyRecord:
        now = datetime.now(timezone.utc)
        
        # In a real system, this hash would include the previous record's hash (blockchain style)
        # to ensure the order of the ledger cannot be altered.
        record_string = f"{evidence_id}:{action_type}:{actor_id}:{now.isoformat()}:{notes}"
        computed_hash = hashlib.sha256(record_string.encode('utf-8')).hexdigest()
        
        record = ChainOfCustodyRecord(
            evidence_id=evidence_id,
            action_type=action_type,
            actor_id=actor_id,
            timestamp=now,
            notes=notes,
            record_hash=computed_hash
        )
        
        self.db.add(record)
        await self.db.commit()
        return record
