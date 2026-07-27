from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.knowledge_graph.managers import EntityManager, RelationshipManager
from app.models.knowledge_graph import EntityStatus, GraphEntity
from app.schemas.knowledge_graph import (
    GraphEntityCreate,
    GraphEntityResponse,
    GraphRelationshipCreate,
    GraphRelationshipResponse,
)

from app.api.api_v1.endpoints import kg_inference, kg_analytics, kg_query

router = APIRouter()

# Core Entity/Relationship endpoints
@router.post("/entities", response_model=GraphEntityResponse)
def create_entity(req: GraphEntityCreate, db: Session = Depends(deps.get_db)):
    manager = EntityManager(db)
    return manager.create_entity(
        entity_type=req.entity_type,
        name=req.name,
        confidence=req.confidence,
        observed_start=req.observed_start,
        observed_end=req.observed_end,
        properties=req.properties_json
    )

@router.get("/entities", response_model=List[GraphEntityResponse])
def list_entities(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return db.query(GraphEntity).filter_by(status=EntityStatus.ACTIVE).offset(skip).limit(limit).all()

@router.post("/relationships", response_model=GraphRelationshipResponse)
def create_relationship(req: GraphRelationshipCreate, db: Session = Depends(deps.get_db)):
    manager = RelationshipManager(db)
    try:
        return manager.create_relationship(
            source_id=req.source_id,
            target_id=req.target_id,
            rel_type=req.relationship_type,
            weight=req.weight,
            confidence=req.confidence,
            is_inferred=req.is_inferred,
            observed_start=req.observed_start,
            observed_end=req.observed_end,
            properties=req.properties_json
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Mount sub-routers for advanced graph operations
router.include_router(kg_inference.router, prefix="/inference", tags=["Knowledge Graph Inference"])
router.include_router(kg_analytics.router, prefix="/analytics", tags=["Knowledge Graph Analytics"])
router.include_router(kg_query.router, prefix="/query", tags=["Knowledge Graph Query"])
