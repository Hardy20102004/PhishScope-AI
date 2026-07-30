import axios from 'axios';
import type {  
  CyberOSOverview, PlatformRegistryEntry, UnifiedObservabilityMetric 
 } from "../types";

export const cyberOsApi = {
  getOverview: async (): Promise<CyberOSOverview> => {
    const response = await axios.get('/api/v1/cyber-os/overview');
    return response.data;
  },
    
  getRegistry: async (skip = 0, limit = 100) => {
    const response = await axios.get(`/api/v1/cyber-os/registry?skip=${skip}&limit=${limit}`);
    return response.data;
  },
    
  getObservability: async (skip = 0, limit = 100) => {
    const response = await axios.get(`/api/v1/cyber-os/observability?skip=${skip}&limit=${limit}`);
    return response.data;
  },
};

