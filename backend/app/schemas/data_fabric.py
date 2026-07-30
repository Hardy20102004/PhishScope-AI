from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.base import APIResponse, PaginationMeta
from app.models.data_fabric import MetadataType, QualityStatus

class MetadataNodeBase(BaseModel):
    name: str = Field(..., description="Name of the metadata node")
    type: MetadataType = Field(..., description="Type of metadata node")
    description: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    owner_id: Optional[UUID] = None
    classification_label: Optional[str] = None

class MetadataNodeCreate(MetadataNodeBase):
    pass

class MetadataNodeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    owner_id: Optional[UUID] = None
    classification_label: Optional[str] = None

class MetadataNode(MetadataNodeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LineageEdgeBase(BaseModel):
    source_node_id: UUID
    target_node_id: UUID
    transformation_type: str
    pipeline_name: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)

class LineageEdgeCreate(LineageEdgeBase):
    pass

class LineageEdge(LineageEdgeBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class QualityMetricBase(BaseModel):
    node_id: UUID
    completeness_score: int = Field(..., ge=0, le=100)
    consistency_score: int = Field(..., ge=0, le=100)
    freshness_score: int = Field(..., ge=0, le=100)
    accuracy_score: int = Field(..., ge=0, le=100)
    overall_status: QualityStatus
    confidence: int = Field(..., ge=0, le=100)
    details: Dict[str, Any] = Field(default_factory=dict)

class QualityMetricCreate(QualityMetricBase):
    pass

class QualityMetric(QualityMetricBase):
    id: UUID
    evaluated_at: datetime

    class Config:
        orm_mode = True

class KnowledgeGraphNode(BaseModel):
    id: str
    label: str
    type: str
    properties: Dict[str, Any] = Field(default_factory=dict)

class KnowledgeGraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship_type: str
    properties: Dict[str, Any] = Field(default_factory=dict)

class KnowledgeGraphView(BaseModel):
    nodes: List[KnowledgeGraphNode]
    edges: List[KnowledgeGraphEdge]

class GovernancePolicyEvaluation(BaseModel):
    node_id: UUID
    policy_name: str
    is_compliant: bool
    violations: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

class DataFabricSummary(BaseModel):
    total_nodes: int
    total_edges: int
    overall_quality_score: int
    critical_issues: int
    summary_text: str
    recommendations: List[str]

class MetadataNodeResponse(APIResponse[MetadataNode]):
    pass

class MetadataNodeListResponse(APIResponse[List[MetadataNode]]):
    pass

class LineageEdgeResponse(APIResponse[LineageEdge]):
    pass

class LineageEdgeListResponse(APIResponse[List[LineageEdge]]):
    pass

class QualityMetricResponse(APIResponse[QualityMetric]):
    pass

class QualityMetricListResponse(APIResponse[List[QualityMetric]]):
    pass
