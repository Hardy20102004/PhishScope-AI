from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.api import deps
from app.knowledge_graph.analytics import GraphAnalyticsEngine

router = APIRouter()

@router.get("/centrality", response_model=List[Dict[str, Any]])
def get_centrality(db: Session = Depends(deps.get_db)):
    engine = GraphAnalyticsEngine(db)
    return engine.calculate_centrality()

@router.get("/clusters", response_model=List[Dict[str, Any]])
def get_clusters(db: Session = Depends(deps.get_db)):
    engine = GraphAnalyticsEngine(db)
    return engine.detect_threat_clusters()
