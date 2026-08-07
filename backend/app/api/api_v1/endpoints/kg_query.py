from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.knowledge_graph.query_engine import GraphQueryEngine
from app.schemas.knowledge_graph import GraphPathResponse

router = APIRouter()

@router.get("/neighbors/{entity_id}", response_model=GraphPathResponse)
def get_neighbors(entity_id: str, depth: int = Query(1, ge=1, le=5), db: Session = Depends(deps.get_db)):
    engine = GraphQueryEngine(db)
    return engine.get_neighbors(entity_id, depth)

@router.get("/shortest-path", response_model=GraphPathResponse)
def shortest_path(source_id: str, target_id: str, db: Session = Depends(deps.get_db)):
    engine = GraphQueryEngine(db)
    return engine.shortest_path(source_id, target_id)
