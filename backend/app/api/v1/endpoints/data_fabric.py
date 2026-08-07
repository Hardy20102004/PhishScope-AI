from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.api import deps
from app.schemas.data_fabric import (
    MetadataNode, MetadataNodeCreate, MetadataNodeUpdate, MetadataNodeResponse, MetadataNodeListResponse,
    LineageEdge, LineageEdgeCreate, LineageEdgeResponse, LineageEdgeListResponse,
    QualityMetric, QualityMetricCreate, QualityMetricResponse, QualityMetricListResponse,
    DataFabricSummary
)
from app.services.data_fabric.manager import SecurityDataFabricManager

router = APIRouter()

@router.get("/overview", response_model=DataFabricSummary)
def get_data_fabric_overview(db: Session = Depends(deps.get_db)) -> Any:
    """Get high-level overview of the Security Data Fabric."""
    manager = SecurityDataFabricManager(db)
    stats = manager.get_overview_stats()
    
    return DataFabricSummary(
        total_nodes=stats["total_metadata_nodes"],
        total_edges=stats["total_lineage_edges"],
        overall_quality_score=stats["overall_quality_score"],
        critical_issues=2, # Mock
        summary_text="The Enterprise Security Data Fabric is operating normally with high data quality.",
        recommendations=["Review 2 critical data quality issues in Identity domains."]
    )

@router.post("/metadata", response_model=MetadataNodeResponse)
def create_metadata_node(
    *,
    db: Session = Depends(deps.get_db),
    node_in: MetadataNodeCreate
) -> Any:
    """Create new metadata node."""
    manager = SecurityDataFabricManager(db)
    node = manager.metadata_catalog.create_node(node_in)
    return {
        "status": "success",
        "data": node,
        "meta": {"request_id": "req-1", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/metadata", response_model=MetadataNodeListResponse)
def get_metadata_nodes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Get all metadata nodes."""
    manager = SecurityDataFabricManager(db)
    nodes = manager.metadata_catalog.get_nodes(skip=skip, limit=limit)
    return {
        "status": "success",
        "data": nodes,
        "meta": {"request_id": "req-2", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.post("/lineage", response_model=LineageEdgeResponse)
def create_lineage_edge(
    *,
    db: Session = Depends(deps.get_db),
    edge_in: LineageEdgeCreate
) -> Any:
    """Create new lineage edge."""
    manager = SecurityDataFabricManager(db)
    edge = manager.data_lineage.create_edge(edge_in)
    return {
        "status": "success",
        "data": edge,
        "meta": {"request_id": "req-3", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.post("/quality", response_model=QualityMetricResponse)
def evaluate_quality(
    *,
    db: Session = Depends(deps.get_db),
    metric_in: QualityMetricCreate
) -> Any:
    """Record a quality metric evaluation."""
    manager = SecurityDataFabricManager(db)
    metric = manager.data_quality.evaluate_quality(metric_in)
    return {
        "status": "success",
        "data": metric,
        "meta": {"request_id": "req-4", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }
