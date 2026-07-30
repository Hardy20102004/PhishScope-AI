export interface DataFabricSummary {
  total_nodes: number;
  total_edges: number;
  overall_quality_score: number;
  critical_issues: number;
  summary_text: string;
  recommendations: string[];
}

export interface MetadataNode {
  id: string;
  name: string;
  type: string;
  description?: string;
  properties: Record<string, any>;
  tags: string[];
  owner_id?: string;
  classification_label?: string;
  created_at: string;
  updated_at: string;
}

export interface LineageEdge {
  id: string;
  source_node_id: string;
  target_node_id: string;
  transformation_type: string;
  pipeline_name?: string;
  details: Record<string, any>;
  created_at: string;
}

export interface QualityMetric {
  id: string;
  node_id: string;
  completeness_score: number;
  consistency_score: number;
  freshness_score: number;
  accuracy_score: number;
  overall_status: string;
  confidence: number;
  details: Record<string, any>;
  evaluated_at: string;
}
