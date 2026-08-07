from sqlalchemy.orm import Session
from app.cloud.models import SharedIntelligenceObject
from loguru import logger
import uuid
from typing import Dict, Any, Optional

class VersionManager:
    """
    Manages versioning of Shared Intelligence Objects to track provenance and detect conflicts.
    """
    def __init__(self, db: Session):
        self.db = db

    def create_new_version(self, entity_id: str, payload: Dict[str, Any], workspace_id: uuid.UUID) -> SharedIntelligenceObject:
        """
        Creates a new version of an intelligence object or increments its version if it exists.
        """
        existing = self.db.query(SharedIntelligenceObject).filter(
            SharedIntelligenceObject.entity_id == entity_id,
            SharedIntelligenceObject.source_workspace_id == workspace_id
        ).order_by(SharedIntelligenceObject.version.desc()).first()
        
        new_version = existing.version + 1 if existing else 1
        
        logger.info(f"Creating version {new_version} for entity {entity_id}")
        
        obj = SharedIntelligenceObject(
            source_workspace_id=workspace_id,
            entity_type=existing.entity_type if existing else "Unknown",
            entity_id=entity_id,
            payload=payload,
            version=new_version,
            tlp_level=existing.tlp_level if existing else "TLP:AMBER"
        )
        
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_latest_version(self, entity_id: str, workspace_id: uuid.UUID) -> Optional[SharedIntelligenceObject]:
        return self.db.query(SharedIntelligenceObject).filter(
            SharedIntelligenceObject.entity_id == entity_id,
            SharedIntelligenceObject.source_workspace_id == workspace_id
        ).order_by(SharedIntelligenceObject.version.desc()).first()
