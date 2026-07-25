from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.knowledge_graph.analytics import GraphAnalyticsEngine
from app.knowledge_graph.inference import InferenceEngine
from app.knowledge_graph.managers import EntityManager, RelationshipManager
from app.knowledge_graph.traversal import TraversalEngine
from app.models.knowledge_graph import EntityStatus, GraphEntity
from app.schemas.knowledge_graph import (
    GraphEntityCreate,
    GraphEntityResponse,
    GraphRelationshipCreate,
    GraphRelationshipResponse,
    SubgraphResponse,
)

router = APIRouter()

@router.post("/entities", response_model=GraphEntityResponse)
def create_entity(req: GraphEntityCreate, db: Session = Depends(deps.get_db)):
    manager = EntityManager(db)
    return manager.create_entity(
        entity_type=req.entity_type,
        name=req.name,
        confidence=req.confidence,
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
            properties=req.properties_json
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/traverse/{entity_id}", response_model=SubgraphResponse)
def get_neighborhood(entity_id: str, depth: int = 1, db: Session = Depends(deps.get_db)):
    engine = TraversalEngine(db)
    subgraph = engine.get_neighborhood(entity_id, depth)
    return SubgraphResponse(
        entities=subgraph["entities"],
        relationships=subgraph["relationships"]
    )

@router.post("/infer")
def trigger_inference(background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)):
    """Triggers asynchronous inference to discover hidden relationships."""
    
    def run_inference():
        # Open a new session for background task
        from app.db.session import SessionLocal
        bg_db = SessionLocal()
        try:
            engine = InferenceEngine(bg_db)
            engine.infer_shared_infrastructure()
        finally:
            bg_db.close()
            
    background_tasks.add_task(run_inference)
    return {"message": "Inference job started in background."}

@router.get("/analytics/centrality")
def get_centrality(db: Session = Depends(deps.get_db)):
    engine = GraphAnalyticsEngine(db)
    centrality = engine.calculate_centrality()
    # Sort descending
    sorted_centrality = dict(sorted(centrality.items(), key=lambda item: item[1], reverse=True)[:50])
    return sorted_centrality
