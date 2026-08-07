import { apiClient } from "./client";

export interface CopilotMessage {
  id: string;
  role: "USER" | "ASSISTANT" | "SYSTEM";
  content: string;
  evidence_references: any[];
  created_at: string;
}

export interface GeneratedReport {
  id: string;
  report_type: string;
  content: string;
  generated_at: string;
}

export const getCopilotHistory = async (investigationId: string): Promise<CopilotMessage[]> => {
  const { data } = await apiClient.get<CopilotMessage[]>(`/copilot/${investigationId}/history`);
  return data;
};

export const sendCopilotMessage = async (investigationId: string, content: string): Promise<CopilotMessage> => {
  const { data } = await apiClient.post<CopilotMessage>(`/copilot/${investigationId}/chat`, { content });
  return data;
};

export const getRecommendations = async (investigationId: string): Promise<string[]> => {
  const { data } = await apiClient.get<{ recommendations: string[] }>(`/copilot/${investigationId}/recommendations`);
  return data.recommendations;
};

export const generateReport = async (investigationId: string, reportType: string): Promise<GeneratedReport> => {
  const { data } = await apiClient.post<GeneratedReport>(`/copilot/${investigationId}/report`, { report_type: reportType });
  return data;
};
