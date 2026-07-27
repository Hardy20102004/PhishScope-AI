from sqlalchemy.orm import Session
from app.cloud.models import FederationNode, FederationSyncRecord
from loguru import logger
import uuid
from typing import List, Optional

class FederationEngine:
    """
    Handles synchronization with external federation nodes (TAXII servers, STIX APIs) and node management.
    """
    def __init__(self, db: Session):
        self.db = db

    def register_node(self, name: str, url: str, node_type: str = "PARTNER", auth_method: str = "MTLS") -> FederationNode:
        logger.info(f"Registering federation node: {name} ({url})")
        node = FederationNode(
            name=name,
            url=url,
            node_type=node_type,
            auth_method=auth_method
        )
        self.db.add(node)
        self.db.commit()
        self.db.refresh(node)
        return node

    def list_nodes(self) -> List[FederationNode]:
        return self.db.query(FederationNode).all()

    def get_node(self, node_id: uuid.UUID) -> Optional[FederationNode]:
        return self.db.query(FederationNode).filter(FederationNode.id == node_id).first()

    def trigger_pull_sync(self, node_id: uuid.UUID) -> FederationSyncRecord:
        """
        Simulates pulling intelligence from a partner node.
        """
        node = self.get_node(node_id)
        if not node:
            raise ValueError("Federation node not found")

        logger.info(f"Triggering TAXII Pull from {node.name} at {node.url}")
        
        # Simulate processing STIX objects
        record = FederationSyncRecord(
            node_id=node_id,
            sync_type="PULL",
            objects_synced=15,
            conflicts_resolved=2,
            status="SUCCESS"
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def trigger_push_sync(self, node_id: uuid.UUID) -> FederationSyncRecord:
        """
        Simulates pushing intelligence to a partner node.
        """
        node = self.get_node(node_id)
        if not node:
            raise ValueError("Federation node not found")

        logger.info(f"Triggering TAXII Push to {node.name} at {node.url}")
        
        record = FederationSyncRecord(
            node_id=node_id,
            sync_type="PUSH",
            objects_synced=8,
            conflicts_resolved=0,
            status="SUCCESS"
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
