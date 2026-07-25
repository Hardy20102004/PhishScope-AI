import uuid
import enum
import structlog
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.ai_memory import MemoryItem, MemoryAuditLog
from app.schemas.ai_memory import MemoryCreate, MemoryUpdate
from app.ai_memory.embeddings import embedding_service, vector_store
from app.ai_memory.compression import MemoryCompressionEngine
from app.ai_memory.graph import RelationshipEngine

logger = structlog.get_logger("phoenix.ai_memory.manager")

class RetentionEngine:
    """
    Enforces TTL, expiration, and deletion policies.
    """
    def __init__(self, db: Session):
        self.db = db

    def apply_retention_policy(self, memory: MemoryItem) -> MemoryItem:
        if memory.retention_policy == "ephemeral":
            memory.expires_at = datetime.utcnow() + timedelta(hours=24)
        elif memory.retention_policy == "session":
            memory.expires_at = datetime.utcnow() + timedelta(days=7)
        else:
            # Persistent memory
            memory.expires_at = None
        return memory
        
    def sweep_expired(self):
        """Runs periodically to delete expired memories from relational and vector stores."""
        now = datetime.utcnow()
        expired = self.db.query(MemoryItem).filter(MemoryItem.expires_at <= now).all()
        for mem in expired:
            if mem.vector_id:
                vector_store.delete(mem.vector_id)
            self.db.delete(mem)
            logger.info("memory_expired_and_purged", memory_id=mem.id)
        self.db.commit()

class MemoryManager:
    """
    Orchestrates the lifecycle of AI Memories.
    Integrates relational storage, vector indexing, graph edges, and auditing.
    """
    def __init__(self, db: Session):
        self.db = db
        self.retention = RetentionEngine(db)
        self.compression = MemoryCompressionEngine()
        self.graph = RelationshipEngine(db)

    def _log_audit(self, memory_id: str, action: str, actor_id: str, details: str = ""):
        log = MemoryAuditLog(
            memory_id=memory_id,
            action_type=action,
            actor_id=actor_id,
            details=details
        )
        self.db.add(log)

    def create_memory(self, data: MemoryCreate, actor_id: str = "system") -> MemoryItem:
        """
        Creates a new memory, generates embeddings, and applies retention policies.
        """
        mem_id = str(uuid.uuid4())
        
        # 1. Compress / Detect Duplicates (Mock)
        if self.compression.detect_duplicates(data.description, []):
            logger.warning("duplicate_memory_detected", title=data.title)
            
        description = self.compression.summarize_context(data.description)
        
        # 2. Generate Semantic Vector
        vector_id = str(uuid.uuid4())
        embedding = embedding_service.generate_embedding(description)
        vector_store.upsert(vector_id, embedding)
        
        # 3. Create Relational Record
        mem = MemoryItem(
            id=mem_id,
            memory_type=data.memory_type.value,
            title=data.title,
            description=description,
            owner_id=data.owner_id,
            case_id=data.case_id,
            investigation_id=data.investigation_id,
            security_classification=data.security_classification.value,
            retention_policy=data.retention_policy,
            confidence_score=data.confidence_score,
            source=data.source,
            vector_id=vector_id
        )
        
        mem = self.retention.apply_retention_policy(mem)
        
        self.db.add(mem)
        self._log_audit(mem_id, "CREATE", actor_id)
        
        self.db.commit()
        self.db.refresh(mem)
        logger.info("memory_created", memory_id=mem_id, type=mem.memory_type)
        return mem

    def get_memory(self, memory_id: str, actor_id: str = "system") -> MemoryItem:
        mem = self.db.query(MemoryItem).filter(MemoryItem.id == memory_id).first()
        if mem:
            self._log_audit(memory_id, "READ", actor_id)
            self.db.commit()
        return mem

    def update_memory(self, memory_id: str, updates: MemoryUpdate, actor_id: str = "system") -> MemoryItem:
        mem = self.db.query(MemoryItem).filter(MemoryItem.id == memory_id).first()
        if not mem:
            raise ValueError("Memory not found")
            
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(mem, key):
                if isinstance(value, enum.Enum):
                    setattr(mem, key, value.value)
                else:
                    setattr(mem, key, value)
                    
        # If description changed, update vector
        if "description" in update_data and mem.vector_id:
            embedding = embedding_service.generate_embedding(update_data["description"])
            vector_store.upsert(mem.vector_id, embedding)
            
        mem.version += 1
        self._log_audit(memory_id, "UPDATE", actor_id, f"Fields updated: {list(update_data.keys())}")
        self.db.commit()
        self.db.refresh(mem)
        return mem
        
    def delete_memory(self, memory_id: str, actor_id: str = "system"):
        mem = self.db.query(MemoryItem).filter(MemoryItem.id == memory_id).first()
        if mem:
            if mem.vector_id:
                vector_store.delete(mem.vector_id)
            self._log_audit(memory_id, "DELETE", actor_id)
            self.db.delete(mem)
            self.db.commit()
            logger.info("memory_deleted", memory_id=memory_id)
