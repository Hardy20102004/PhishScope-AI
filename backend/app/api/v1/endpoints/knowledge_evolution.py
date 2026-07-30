from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.api import deps
from app.schemas.knowledge_evolution import (
    OntologyNode, OntologyNodeCreate, OntologyNodeUpdate, OntologyNodeResponse, OntologyNodeListResponse,
    SchemaRecommendation, SchemaRecommendationCreate, SchemaRecommendationResponse, SchemaRecommendationListResponse,
    EvolutionQualityMetric, EvolutionQualityMetricCreate, EvolutionQualityMetricResponse,
    KnowledgeEvolutionSummary, DiscoveredRelationship
)
from app.services.knowledge_evolution.manager import KnowledgeEvolutionManager

router = APIRouter()

@router.get("/overview", response_model=KnowledgeEvolutionSummary)
def get_evolution_overview(db: Session = Depends(deps.get_db)) -> Any:
    """Get high-level overview of the Knowledge Evolution Platform."""
    manager = KnowledgeEvolutionManager(db)
    stats = manager.get_overview_stats()
    
    return KnowledgeEvolutionSummary(
        total_ontology_nodes=stats["total_ontology_nodes"],
        pending_recommendations=stats["pending_recommendations"],
        overall_quality_score=stats["overall_quality_score"],
        summary_text="Knowledge Evolution is actively discovering new relationships and maintaining ontology compliance.",
        recommendations=["Review 3 pending schema recommendations for Cloud assets."]
    )

@router.post("/ontology", response_model=OntologyNodeResponse)
def create_ontology_node(
    *,
    db: Session = Depends(deps.get_db),
    node_in: OntologyNodeCreate
) -> Any:
    """Create new ontology node."""
    manager = KnowledgeEvolutionManager(db)
    node = manager.ontology.create_node(node_in)
    return {
        "status": "success",
        "data": node,
        "meta": {"request_id": "req-1", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/ontology", response_model=OntologyNodeListResponse)
def get_ontology_nodes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Get all ontology nodes."""
    manager = KnowledgeEvolutionManager(db)
    nodes = manager.ontology.get_nodes(skip=skip, limit=limit)
    return {
        "status": "success",
        "data": nodes,
        "meta": {"request_id": "req-2", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.post("/ontology/{node_id}/approve", response_model=OntologyNodeResponse)
def approve_ontology_node(
    *,
    db: Session = Depends(deps.get_db),
    node_id: UUID
) -> Any:
    """Approve an ontology node (Mock user ID)."""
    manager = KnowledgeEvolutionManager(db)
    node = manager.ontology.approve_node(node_id, user_id=UUID("00000000-0000-0000-0000-000000000000"))
    if not node:
        raise HTTPException(status_code=404, detail="Ontology node not found")
    return {
        "status": "success",
        "data": node,
        "meta": {"request_id": "req-3", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/relationships/discover", response_model=Any)
def discover_relationships(
    db: Session = Depends(deps.get_db)
) -> Any:
    """Discover new relationships."""
    manager = KnowledgeEvolutionManager(db)
    relationships = manager.discovery.discover_relationships()
    return {
        "status": "success",
        "data": relationships,
        "meta": {"request_id": "req-4", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/recommendations", response_model=SchemaRecommendationListResponse)
def get_schema_recommendations(
    db: Session = Depends(deps.get_db)
) -> Any:
    """Get pending schema recommendations."""
    manager = KnowledgeEvolutionManager(db)
    recommendations = manager.schema.get_pending_recommendations()
    return {
        "status": "success",
        "data": recommendations,
        "meta": {"request_id": "req-5", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }
