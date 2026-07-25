import { apiClient } from "./client";

export interface ThreatFeedResult {
  id: string;
  source: string;
  reputation_score: number;
  confidence: number;
  threat_classification: string | null;
  raw_data?: any;
  is_cached: boolean;
  created_at: string;
}

export interface Indicator {
  id: string;
  value: string;
  type: string;
  normalized_value: string;
  reputation_score: number;
  confidence_score: number;
  threat_classification: string | null;
  first_seen: string;
  last_seen: string;
  last_updated: string;
  observation_count: number;
  feed_results: ThreatFeedResult[];
}

export const getIndicator = async (value: string, forceRefresh = false): Promise<Indicator> => {
  const { data } = await apiClient.get<Indicator>(`/threat-intel/indicators/${encodeURIComponent(value)}`, {
    params: { force_refresh: forceRefresh }
  });
  return data;
};

export const searchIndicator = async (value: string): Promise<Indicator> => {
  const { data } = await apiClient.post<Indicator>("/threat-intel/indicators/search", { value });
  return data;
};

export const getFeedsStatus = async (): Promise<any> => {
  const { data } = await apiClient.get("/threat-intel/feeds/status");
  return data;
};
