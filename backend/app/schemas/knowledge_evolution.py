from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.base import APIResponse
from app.models.knowledge_evolution import OntologyType, ApprovalStatus

class OntologyNodeBase(BaseModel):
    name: str = Field(..., description="Name of the ontology node (e.g. Entity Type)")
    type: OntologyType
    description: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    schema_version: str = "1.0"

class OntologyNodeCreate(OntologyNodeBase):
    pass

class OntologyNodeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    schema_version: Optional[str] = None
    status: Optional[ApprovalStatus] = None

class OntologyNode(OntologyNodeBase):
    id: UUID
    status: ApprovalStatus
    approved_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SchemaRecommendationBase(BaseModel):
    target_node_id: Optional[UUID] = None
    recommendation_type: str
    description: str
    evidence: Dict[str, Any] = Field(default_factory=dict)

class SchemaRecommendationCreate(SchemaRecommendationBase):
    pass

class SchemaRecommendation(SchemaRecommendationBase):
    id: UUID
    status: ApprovalStatus
    created_at: datetime

    class Config:
        from_attributes = True

class EvolutionQualityMetricBase(BaseModel):
    coverage_score: int = Field(..., ge=0, le=100)
    consistency_score: int = Field(..., ge=0, le=100)
    freshness_score: int = Field(..., ge=0, le=100)
    confidence_score: int = Field(..., ge=0, le=100)
    relationship_quality: int = Field(..., ge=0, le=100)
    details: Dict[str, Any] = Field(default_factory=dict)

class EvolutionQualityMetricCreate(EvolutionQualityMetricBase):
    pass

class EvolutionQualityMetric(EvolutionQualityMetricBase):
    id: UUID
    evaluated_at: datetime

    class Config:
        from_attributes = True

class KnowledgeEvolutionSummary(BaseModel):
    total_ontology_nodes: int
    pending_recommendations: int
    overall_quality_score: int
    summary_text: str
    recommendations: List[str]

class DiscoveredRelationship(BaseModel):
    source_entity: str
    target_entity: str
    relationship_type: str
    confidence: float
    evidence: str
    is_inferred: bool = True

class OntologyNodeResponse(APIResponse[OntologyNode]):
    pass

class OntologyNodeListResponse(APIResponse[List[OntologyNode]]):
    pass

class SchemaRecommendationResponse(APIResponse[SchemaRecommendation]):
    pass

class SchemaRecommendationListResponse(APIResponse[List[SchemaRecommendation]]):
    pass

class EvolutionQualityMetricResponse(APIResponse[EvolutionQualityMetric]):
    pass
