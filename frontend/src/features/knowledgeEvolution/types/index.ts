export interface OntologyNode {
  id: string;
  name: string;
  type: "ENTITY_TYPE" | "RELATIONSHIP_TYPE" | "TAXONOMY" | "SEMANTIC_MODEL";
  description?: string;
  properties: Record<string, any>;
  schema_version: string;
  status: "PENDING" | "APPROVED" | "REJECTED";
  approved_by?: string;
  created_at: string;
  updated_at: string;
}

export interface SchemaRecommendation {
  id: string;
  target_node_id?: string;
  recommendation_type: string;
  description: string;
  evidence: Record<string, any>;
  status: "PENDING" | "APPROVED" | "REJECTED";
  created_at: string;
}

export interface EvolutionQualityMetric {
  id: string;
  coverage_score: number;
  consistency_score: number;
  freshness_score: number;
  confidence_score: number;
  relationship_quality: number;
  details: Record<string, any>;
  evaluated_at: string;
}

export interface KnowledgeEvolutionSummary {
  total_ontology_nodes: number;
  pending_recommendations: number;
  overall_quality_score: number;
  summary_text: string;
  recommendations: string[];
}

export interface DiscoveredRelationship {
  source_entity: string;
  target_entity: string;
  relationship_type: string;
  confidence: number;
  evidence: string;
  is_inferred: boolean;
}
