from sqlalchemy.orm import Session
from app.cloud.federation import FederationEngine
from app.cloud.conflict_resolution import ConflictResolutionEngine
from app.cloud.models import FederationNode
import uuid
from loguru import logger
import time

class SynchronizationEngine:
    """
    Manages complex synchronizations, retries, and offline states.
    """
    def __init__(self, db: Session):
        self.db = db
        self.federation = FederationEngine(db)
        self.conflict_resolution = ConflictResolutionEngine(db)

    def trigger_full_sync(self, node_id: uuid.UUID):
        logger.info(f"Triggering Full Sync for node {node_id}")
        node = self.federation.get_node(node_id)
        if not node:
            raise ValueError("Node not found")
            
        if not node.is_active:
            logger.warning(f"Node {node_id} is inactive. Queuing for offline synchronization.")
            return False
            
        # Push then Pull
        self.federation.trigger_push_sync(node_id)
        time.sleep(1) # Simulate network delay
        self.federation.trigger_pull_sync(node_id)
        
        logger.info(f"Full Sync for node {node_id} completed.")
        return True

    def trigger_incremental_sync(self, node_id: uuid.UUID):
        logger.info(f"Triggering Incremental Sync for node {node_id}")
        return self.federation.trigger_pull_sync(node_id)
