import { api } from '@/lib/api';
import { 
  CyberOSOverview, PlatformRegistryEntry, UnifiedObservabilityMetric 
} from '../types';

export const cyberOsApi = {
  getOverview: () => 
    api.get<CyberOSOverview>('/api/v1/cyber-os/overview'),
    
  getRegistry: (skip = 0, limit = 100) =>
    api.get<{status: string, data: PlatformRegistryEntry[], meta: any}>(`/api/v1/cyber-os/registry?skip=${skip}&limit=${limit}`),
    
  getObservability: (skip = 0, limit = 100) =>
    api.get<{status: string, data: UnifiedObservabilityMetric[], meta: any}>(`/api/v1/cyber-os/observability?skip=${skip}&limit=${limit}`),
};
