from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.attack_graph.schemas import (
    GraphPayload,
    AttackPathResponse,
    ImpactAnalysisResponse,
    GraphSnapshotCreate,
    GraphSnapshotResponse
)
from app.attack_graph.models import GraphSnapshot
from app.attack_graph.builder import AttackGraphBuilder
from app.attack_graph.path_discovery import PathDiscoveryEngine
from app.attack_graph.impact import ImpactAnalysisEngine
from app.attack_graph.analytics import GraphAnalyticsEngine

router = APIRouter()

@router.get("/build", response_model=GraphPayload)
def build_attack_graph(
    seed_id: str,
    depth: int = 2,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Build a dynamic attack graph around a seed entity.
    """
    builder = AttackGraphBuilder(db)
    return builder.build_subgraph(seed_entity_id=seed_id, depth=depth)

@router.get("/path", response_model=AttackPathResponse)
def get_attack_path(
    source_id: str,
    target_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Calculate the critical path between two entities.
    """
    engine = PathDiscoveryEngine(db)
    return engine.calculate_shortest_path(source_id, target_id)

@router.get("/impact/{entity_id}", response_model=ImpactAnalysisResponse)
def get_node_impact(
    entity_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get centrality and impact metrics for a specific node.
    """
    engine = ImpactAnalysisEngine(db)
    return engine.calculate_node_impact(entity_id)

@router.get("/analytics/summary")
def get_graph_analytics(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get high-level attack graph analytics.
    """
    engine = GraphAnalyticsEngine(db)
    return engine.get_summary_metrics()

@router.post("/snapshot", response_model=GraphSnapshotResponse)
def save_graph_snapshot(
    snapshot_in: GraphSnapshotCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    snapshot = GraphSnapshot(
        name=snapshot_in.name,
        description=snapshot_in.description,
        graph_data=snapshot_in.graph_data.model_dump()
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot
