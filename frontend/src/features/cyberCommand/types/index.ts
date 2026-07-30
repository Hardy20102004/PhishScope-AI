export interface EnterpriseHealthMetric {
  id: string;
  domain: string;
  health_score: number;
  status: "ACTIVE" | "DEGRADED" | "CRITICAL" | "OFFLINE";
  details: Record<string, any>;
  evaluated_at: string;
}

export interface StrategicPlan {
  id: string;
  title: string;
  description: string;
  horizon: string;
  milestones: any[];
  budget_allocation?: number;
  created_at: string;
  updated_at: string;
}

export interface ExecutiveCopilotSummary {
  id: string;
  context_window: string;
  observed_evidence: Record<string, any>;
  calculated_metrics: Record<string, any>;
  strategic_recommendations: string[];
  generated_at: string;
}

export interface CyberCommandOverview {
  global_health_score: number;
  active_operations_count: number;
  critical_alerts: number;
  strategic_alignment_score: number;
  ai_strategic_briefing: string;
}
