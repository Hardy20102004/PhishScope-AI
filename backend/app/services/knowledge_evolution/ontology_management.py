from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.knowledge_evolution import OntologyNode, ApprovalStatus
from app.schemas.knowledge_evolution import OntologyNodeCreate, OntologyNodeUpdate

class OntologyManagementEngine:
    def __init__(self, db: Session):
        self.db = db

    def create_node(self, node_in: OntologyNodeCreate) -> OntologyNode:
        db_node = OntologyNode(
            name=node_in.name,
            type=node_in.type,
            description=node_in.description,
            properties=node_in.properties,
            schema_version=node_in.schema_version,
            status=ApprovalStatus.PENDING # Requires explicit human approval
        )
        self.db.add(db_node)
        self.db.commit()
        self.db.refresh(db_node)
        return db_node

    def get_node(self, node_id: UUID) -> Optional[OntologyNode]:
        return self.db.query(OntologyNode).filter(OntologyNode.id == node_id).first()

    def get_nodes(self, skip: int = 0, limit: int = 100) -> List[OntologyNode]:
        return self.db.query(OntologyNode).offset(skip).limit(limit).all()

    def approve_node(self, node_id: UUID, user_id: UUID) -> Optional[OntologyNode]:
        db_node = self.get_node(node_id)
        if db_node:
            db_node.status = ApprovalStatus.APPROVED
            db_node.approved_by = user_id
            self.db.add(db_node)
            self.db.commit()
            self.db.refresh(db_node)
        return db_node
