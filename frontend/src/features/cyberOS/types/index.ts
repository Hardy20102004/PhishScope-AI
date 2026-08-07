export interface PlatformRegistryEntry {
  id: string;
  module_name: string;
  version: string;
  api_endpoint_prefix: string;
  status: "ONLINE" | "DEGRADED" | "OFFLINE" | "MAINTENANCE";
  capabilities: string[];
  registered_at: string;
  last_heartbeat: string;
}

export interface UnifiedObservabilityMetric {
  id: string;
  metric_type: string;
  value: number;
  unit: string;
  source_module: string;
  timestamp: string;
}

export interface CyberOSOverview {
  kernel_status: string;
  registered_modules_count: number;
  global_cpu_usage: number;
  global_memory_usage: number;
  active_alerts: number;
  ai_status: string;
}
