import { apiClient } from "./client";

export interface Report {
  id: string;
  title: string;
  case_id?: string;
  investigation_id?: string;
  template_id?: string;
  content_data: any;
  rendered_html?: string;
  status: "DRAFT" | "UNDER_REVIEW" | "APPROVED" | "PUBLISHED" | "ARCHIVED";
  created_at: string;
  updated_at: string;
}

export interface ExportRecord {
  id: string;
  target_id: string;
  target_type: string;
  format: "JSON" | "CSV" | "PDF" | "HTML" | "MARKDOWN" | "ZIP";
  file_hash?: string;
  created_at: string;
}

export interface EvidenceManifest {
  id: string;
  case_id: string;
  manifest_json: any;
  hash_value: string;
  created_at: string;
}

export const listReports = async (caseId?: string): Promise<Report[]> => {
  const params = caseId ? { case_id: caseId } : {};
  const { data } = await apiClient.get<Report[]>("/reports/", { params });
  return data;
};

export const createReport = async (reportData: Partial<Report>): Promise<Report> => {
  const { data } = await apiClient.post<Report>("/reports/generate", reportData);
  return data;
};

export const updateReportStatus = async (id: string, status: string): Promise<Report> => {
  const { data } = await apiClient.patch<Report>(`/reports/${id}/status`, { status });
  return data;
};

export const exportCase = async (caseId: string, format: string): Promise<ExportRecord> => {
  const { data } = await apiClient.post<ExportRecord>(`/reports/cases/${caseId}/export`, { format, include_evidence: true });
  return data;
};

export const generateManifest = async (caseId: string): Promise<EvidenceManifest> => {
  const { data } = await apiClient.post<EvidenceManifest>(`/reports/cases/${caseId}/manifest`);
  return data;
};

export const verifyManifest = async (manifest_json: any, hash_value: string): Promise<{ valid: boolean }> => {
  const { data } = await apiClient.post<{ valid: boolean }>("/reports/verify", { manifest_json, hash_value });
  return data;
};
