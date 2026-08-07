from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.data_fabric import LineageEdge, MetadataNode
from app.schemas.data_fabric import LineageEdgeCreate

class DataLineageEngine:
    def __init__(self, db: Session):
        self.db = db

    def create_edge(self, edge_in: LineageEdgeCreate) -> LineageEdge:
        db_edge = LineageEdge(
            source_node_id=edge_in.source_node_id,
            target_node_id=edge_in.target_node_id,
            transformation_type=edge_in.transformation_type,
            pipeline_name=edge_in.pipeline_name,
            details=edge_in.details
        )
        self.db.add(db_edge)
        self.db.commit()
        self.db.refresh(db_edge)
        return db_edge

    def get_upstream_lineage(self, target_node_id: UUID) -> List[LineageEdge]:
        # Simple one-level upstream for now
        return self.db.query(LineageEdge).filter(LineageEdge.target_node_id == target_node_id).all()

    def get_downstream_lineage(self, source_node_id: UUID) -> List[LineageEdge]:
        # Simple one-level downstream for now
        return self.db.query(LineageEdge).filter(LineageEdge.source_node_id == source_node_id).all()
