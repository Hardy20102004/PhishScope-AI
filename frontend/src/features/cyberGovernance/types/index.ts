export interface CyberGovernanceKPI {
  id: string;
  metric_name: string;
  metric_value: number;
  target_value: number;
  category: string;
  evaluated_at: string;
}

export interface GovernancePolicy {
  id: string;
  name: string;
  description?: string;
  version: string;
  framework: string;
  status: "DRAFT" | "ACTIVE" | "RETIRED" | "IN_REVIEW";
  created_at: string;
  updated_at: string;
  next_review_date?: string;
}

export interface RiskOversightMetric {
  id: string;
  risk_domain: string;
  risk_score: number;
  confidence_level: number;
  details: Record<string, any>;
  evaluated_at: string;
}

export interface BoardReportSummary {
  id: string;
  title: string;
  quarter: string;
  summary_text: string;
  investment_summary: Record<string, any>;
  risk_summary: Record<string, any>;
  generated_by_ai: boolean;
  created_at: string;
}

export interface CyberGovernanceOverview {
  overall_maturity_score: number;
  active_policies_count: number;
  critical_risks_count: number;
  board_reports_generated: number;
  ai_recommendations: string[];
}
