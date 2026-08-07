import { apiClient } from "./client";

export interface WorkflowVersion {
  version_number: number;
  definition_json: any;
  created_at: string;
}

export interface Workflow {
  id: string;
  name: string;
  description?: string;
  trigger_type: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  versions: WorkflowVersion[];
}

export interface WorkflowExecution {
  id: string;
  version_id: string;
  trigger_event_json: any;
  status: "PENDING" | "RUNNING" | "COMPLETED" | "FAILED";
  logs_json: any[];
  started_at: string;
  completed_at?: string;
}

export const listWorkflows = async (): Promise<Workflow[]> => {
  const { data } = await apiClient.get<Workflow[]>("/automation/workflows");
  return data;
};

export const createWorkflow = async (workflowData: any): Promise<Workflow> => {
  const { data } = await apiClient.post<Workflow>("/automation/workflows", workflowData);
  return data;
};

export const executeWorkflow = async (workflowId: string, payload: any): Promise<WorkflowExecution> => {
  const { data } = await apiClient.post<WorkflowExecution>(`/automation/workflows/${workflowId}/execute`, payload);
  return data;
};

export const getExecutionLogs = async (executionId: string): Promise<WorkflowExecution> => {
  const { data } = await apiClient.get<WorkflowExecution>(`/automation/executions/${executionId}`);
  return data;
};
