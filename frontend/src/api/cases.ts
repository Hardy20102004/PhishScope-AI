import { apiClient } from "./client";

export interface CaseTask {
  id: string;
  title: string;
  description: string;
  status: "TODO" | "IN_PROGRESS" | "DONE";
  assignee_id?: string;
  created_at: string;
  updated_at: string;
}

export interface CaseDecision {
  id: string;
  decision: string;
  reasoning: string;
  confidence_score: number;
  evidence_references: any[];
  created_at: string;
  user_id: string;
}

export interface Case {
  id: string;
  title: string;
  description?: string;
  status: "OPEN" | "IN_PROGRESS" | "PENDING" | "CLOSED";
  priority: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  tags: string[];
  owner_id?: string;
  created_at: string;
  updated_at: string;
  tasks: CaseTask[];
  decisions?: CaseDecision[];
}

export const listCases = async (): Promise<Case[]> => {
  const { data } = await apiClient.get<Case[]>("/cases/");
  return data;
};

export const createCase = async (caseData: Partial<Case>): Promise<Case> => {
  const { data } = await apiClient.post<Case>("/cases/", caseData);
  return data;
};

export const getCase = async (id: string): Promise<Case> => {
  const { data } = await apiClient.get<Case>(`/cases/${id}`);
  return data;
};

export const updateCase = async (id: string, updates: Partial<Case>): Promise<Case> => {
  const { data } = await apiClient.patch<Case>(`/cases/${id}`, updates);
  return data;
};

export const linkInvestigation = async (caseId: string, investigationId: string): Promise<void> => {
  await apiClient.post(`/cases/${caseId}/link-investigation/${investigationId}`);
};
