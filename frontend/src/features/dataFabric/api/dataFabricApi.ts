import { apiClient } from '@/api/client';
import type {  DataFabricSummary, MetadataNode, LineageEdge, QualityMetric  } from "../types";

const API_BASE_URL = '/data-fabric';

export const dataFabricApi = {
  getOverview: async (): Promise<DataFabricSummary> => {
    const response = await apiClient.get(`${API_BASE_URL}/overview`);
    return response.data;
  },

  getMetadataNodes: async (skip = 0, limit = 100): Promise<MetadataNode[]> => {
    const response = await apiClient.get(`${API_BASE_URL}/metadata`, { params: { skip, limit } });
    return response.data.data;
  },
  
  createMetadataNode: async (node: Partial<MetadataNode>): Promise<MetadataNode> => {
    const response = await apiClient.post(`${API_BASE_URL}/metadata`, node);
    return response.data.data;
  },
};
