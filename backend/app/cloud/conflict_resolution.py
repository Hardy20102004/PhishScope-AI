from sqlalchemy.orm import Session
from app.cloud.models import ConflictRecord
from loguru import logger
import uuid
from typing import List, Optional

class ConflictResolutionEngine:
    """
    Detects and resolves synchronization conflicts.
    """
    def __init__(self, db: Session):
        self.db = db

    def register_conflict(self, entity_id: str, entity_type: str, local_version: int, remote_version: int) -> ConflictRecord:
        logger.warning(f"Conflict detected for {entity_type} {entity_id}: Local v{local_version} vs Remote v{remote_version}")
        conflict = ConflictRecord(
            entity_id=entity_id,
            entity_type=entity_type,
            local_version=local_version,
            remote_version=remote_version,
            status="PENDING",
            resolution_strategy="MANUAL_MERGE"
        )
        self.db.add(conflict)
        self.db.commit()
        self.db.refresh(conflict)
        return conflict

    def resolve_conflict(self, conflict_id: uuid.UUID, strategy: str) -> bool:
        """
        Resolves a conflict using a chosen strategy (KEEP_LOCAL, ACCEPT_REMOTE).
        """
        conflict = self.db.query(ConflictRecord).filter(ConflictRecord.id == conflict_id).first()
        if not conflict:
            return False
            
        logger.info(f"Resolving conflict {conflict_id} using {strategy}")
        conflict.resolution_strategy = strategy
        conflict.status = "RESOLVED"
        self.db.commit()
        return True

    def get_pending_conflicts(self) -> List[ConflictRecord]:
        return self.db.query(ConflictRecord).filter(ConflictRecord.status == "PENDING").all()
