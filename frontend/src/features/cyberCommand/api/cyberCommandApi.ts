import { api } from '@/lib/api';
import { 
  CyberCommandOverview, EnterpriseHealthMetric, StrategicPlan 
} from '../types';

export const cyberCommandApi = {
  getOverview: () => 
    api.get<CyberCommandOverview>('/api/v1/cyber-command/overview'),
    
  getEnterpriseHealth: (skip = 0, limit = 100) =>
    api.get<{status: string, data: EnterpriseHealthMetric[], meta: any}>(`/api/v1/cyber-command/health?skip=${skip}&limit=${limit}`),
    
  getStrategicPlans: (skip = 0, limit = 100) =>
    api.get<{status: string, data: StrategicPlan[], meta: any}>(`/api/v1/cyber-command/strategy/plans?skip=${skip}&limit=${limit}`),
};
