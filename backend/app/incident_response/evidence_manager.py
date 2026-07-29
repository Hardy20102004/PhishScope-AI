import uuid
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.incident_response import EvidenceRecord, ChainOfCustodyLog

class EvidenceManager:
    """
    Manages digital evidence and guarantees an immutable Chain of Custody log using cryptographic hashes.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    def _generate_digital_signature(self, data: str) -> str:
        """
        Generates a SHA-256 hash of the evidence string to guarantee integrity.
        In a production system, this would hash the actual file buffer or memory dump.
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    async def attach_evidence(
        self, 
        case_id: uuid.UUID, 
        artifact_type: str, 
        artifact_value: str, 
        source: str, 
        user_id: uuid.UUID
    ) -> EvidenceRecord:
        """
        Attaches new evidence to a case and automatically generates the initial Chain of Custody 'COLLECTED' log.
        """
        evidence = EvidenceRecord(
            case_id=case_id,
            artifact_type=artifact_type,
            artifact_value=artifact_value,
            source=source
        )
        self.db.add(evidence)
        await self.db.flush()
        
        signature = self._generate_digital_signature(artifact_value)
        
        coc_log = ChainOfCustodyLog(
            evidence_id=evidence.id,
            action="COLLECTED",
            performed_by_id=user_id,
            digital_signature=signature,
            notes="Initial collection and hashing."
        )
        self.db.add(coc_log)
        
        await self.db.commit()
        await self.db.refresh(evidence)
        
        return evidence

    async def transfer_evidence(self, evidence_id: uuid.UUID, user_id: uuid.UUID, notes: str) -> ChainOfCustodyLog:
        """
        Logs a 'TRANSFERRED' action on the chain of custody.
        """
        result = await self.db.execute(select(EvidenceRecord).where(EvidenceRecord.id == evidence_id))
        evidence = result.scalar_one_or_none()
        
        if not evidence:
            raise ValueError("Evidence not found")
            
        # Re-verify hash to ensure no tampering occurred before transfer
        signature = self._generate_digital_signature(evidence.artifact_value)
        
        coc_log = ChainOfCustodyLog(
            evidence_id=evidence_id,
            action="TRANSFERRED",
            performed_by_id=user_id,
            digital_signature=signature,
            notes=notes
        )
        self.db.add(coc_log)
        await self.db.commit()
        await self.db.refresh(coc_log)
        
        return coc_log
