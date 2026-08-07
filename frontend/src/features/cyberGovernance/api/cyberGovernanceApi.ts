import { api } from '@/lib/api';
import type {  
  CyberGovernanceOverview, GovernancePolicy, BoardReportSummary 
 } from "../types";

export const cyberGovernanceApi = {
  getOverview: () => 
    api.get<CyberGovernanceOverview>('/api/v1/cyber-governance/overview'),
    
  getPolicies: (skip = 0, limit = 100) =>
    api.get<{status: string, data: GovernancePolicy[], meta: any}>(`/api/v1/cyber-governance/policies?skip=${skip}&limit=${limit}`),
    
  createPolicy: (policy: Partial<GovernancePolicy>) =>
    api.post<{status: string, data: GovernancePolicy, meta: any}>('/api/v1/cyber-governance/policies', policy),
    
  getBoardReports: (skip = 0, limit = 100) =>
    api.get<{status: string, data: BoardReportSummary[], meta: any}>(`/api/v1/cyber-governance/board-reports?skip=${skip}&limit=${limit}`),
};
