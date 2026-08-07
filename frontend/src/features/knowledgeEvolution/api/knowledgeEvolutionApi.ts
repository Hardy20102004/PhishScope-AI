import { api } from '@/lib/api';
import type {  OntologyNode, SchemaRecommendation, KnowledgeEvolutionSummary, DiscoveredRelationship  } from "../types";

export const knowledgeEvolutionApi = {
  getOverview: () => 
    api.get<KnowledgeEvolutionSummary>('/api/v1/knowledge-evolution/overview'),
    
  getOntologyNodes: (skip = 0, limit = 100) =>
    api.get<{status: string, data: OntologyNode[], meta: any}>(`/api/v1/knowledge-evolution/ontology?skip=${skip}&limit=${limit}`),
    
  createOntologyNode: (node: Partial<OntologyNode>) =>
    api.post<{status: string, data: OntologyNode, meta: any}>('/api/v1/knowledge-evolution/ontology', node),
    
  approveOntologyNode: (nodeId: string) =>
    api.post<{status: string, data: OntologyNode, meta: any}>(`/api/v1/knowledge-evolution/ontology/${nodeId}/approve`),
    
  getRecommendations: () =>
    api.get<{status: string, data: SchemaRecommendation[], meta: any}>('/api/v1/knowledge-evolution/recommendations'),
    
  discoverRelationships: () =>
    api.get<{status: string, data: DiscoveredRelationship[], meta: any}>('/api/v1/knowledge-evolution/relationships/discover'),
};
