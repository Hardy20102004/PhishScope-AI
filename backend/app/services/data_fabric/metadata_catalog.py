from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.data_fabric import MetadataNode
from app.schemas.data_fabric import MetadataNodeCreate, MetadataNodeUpdate

class MetadataCatalogEngine:
    def __init__(self, db: Session):
        self.db = db

    def create_node(self, node_in: MetadataNodeCreate) -> MetadataNode:
        db_node = MetadataNode(
            name=node_in.name,
            type=node_in.type,
            description=node_in.description,
            properties=node_in.properties,
            tags=node_in.tags,
            owner_id=node_in.owner_id,
            classification_label=node_in.classification_label
        )
        self.db.add(db_node)
        self.db.commit()
        self.db.refresh(db_node)
        return db_node

    def get_node(self, node_id: UUID) -> Optional[MetadataNode]:
        return self.db.query(MetadataNode).filter(MetadataNode.id == node_id).first()

    def get_nodes(self, skip: int = 0, limit: int = 100) -> List[MetadataNode]:
        return self.db.query(MetadataNode).offset(skip).limit(limit).all()

    def update_node(self, node_id: UUID, node_in: MetadataNodeUpdate) -> Optional[MetadataNode]:
        db_node = self.get_node(node_id)
        if not db_node:
            return None
        
        update_data = node_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_node, key, value)
            
        self.db.add(db_node)
        self.db.commit()
        self.db.refresh(db_node)
        return db_node

    def delete_node(self, node_id: UUID) -> bool:
        db_node = self.get_node(node_id)
        if not db_node:
            return False
        self.db.delete(db_node)
        self.db.commit()
        return True
