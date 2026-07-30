import axios from 'axios';
import type {  DataFabricSummary, MetadataNode, LineageEdge, QualityMetric  } from "../types";

const API_BASE_URL = '/api/v1/data-fabric';

export const dataFabricApi = {
  getOverview: async (): Promise<DataFabricSummary> => {
    const response = await axios.get(`${API_BASE_URL}/overview`);
    return response.data;
  },

  getMetadataNodes: async (skip = 0, limit = 100): Promise<MetadataNode[]> => {
    const response = await axios.get(`${API_BASE_URL}/metadata`, { params: { skip, limit } });
    return response.data.data;
  },
  
  createMetadataNode: async (node: Partial<MetadataNode>): Promise<MetadataNode> => {
    const response = await axios.post(`${API_BASE_URL}/metadata`, node);
    return response.data.data;
  },
};
