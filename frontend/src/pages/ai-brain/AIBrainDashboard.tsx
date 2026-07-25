import { useState, useEffect } from "react"
import { Activity, Cpu, ShieldCheck, Database, Zap, RefreshCw } from "lucide-react"

export default function AIBrainDashboard() {
  const [metrics, setMetrics] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate API fetch from backend/api/v1/ai-brain/health-analytics
    setTimeout(() => {
      setMetrics({
        status: "OPERATIONAL",
        provider_health: [
          { name: "Claude", circuit_state: "CLOSED" },
          { name: "Gemini", circuit_state: "CLOSED" },
          { name: "OpenAI", circuit_state: "CLOSED" },
          { name: "Ollama Local", circuit_state: "CLOSED" }
        ],
        telemetry_metrics: {
          total_input_tokens_24h: 42500,
          total_output_tokens_24h: 18900,
          estimated_cost_usd_24h: 0.3472,
          average_latency_ms: 640,
          failover_rate_percent: 0.02,
          hallucination_prevention_blocks_24h: 3
        }
      })
      setLoading(false)
    }, 800)
  }, [])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">AI Security Brain</h1>
          <p className="text-muted-foreground mt-1">Enterprise Command Center & Orchestration Hub</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="flex h-3 w-3 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
          </span>
          <span className="text-sm font-semibold text-emerald-500">ALL SYSTEMS NOMINAL</span>
        </div>
      </div>

      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <RefreshCw className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-md">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-muted-foreground">Tokens Analyzed (24h)</h3>
              <Database className="h-4 w-4 text-blue-500" />
            </div>
            <div className="mt-4 flex items-baseline gap-2">
              <span className="text-3xl font-bold">{(metrics.telemetry_metrics.total_input_tokens_24h / 1000).toFixed(1)}k</span>
              <span className="text-xs font-medium text-emerald-500">+12.5%</span>
            </div>
          </div>

          <div className="rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-md">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-muted-foreground">Orchestration Latency</h3>
              <Zap className="h-4 w-4 text-amber-500" />
            </div>
            <div className="mt-4 flex items-baseline gap-2">
              <span className="text-3xl font-bold">{metrics.telemetry_metrics.average_latency_ms}ms</span>
              <span className="text-xs font-medium text-emerald-500">-40ms</span>
            </div>
          </div>

          <div className="rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-md">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-muted-foreground">Active Providers</h3>
              <Cpu className="h-4 w-4 text-indigo-500" />
            </div>
            <div className="mt-4 flex items-baseline gap-2">
              <span className="text-3xl font-bold">{metrics.provider_health.length}</span>
              <span className="text-xs font-medium text-muted-foreground">Failover Enabled</span>
            </div>
          </div>

          <div className="rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-md">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-muted-foreground">Governance Blocks</h3>
              <ShieldCheck className="h-4 w-4 text-rose-500" />
            </div>
            <div className="mt-4 flex items-baseline gap-2">
              <span className="text-3xl font-bold">{metrics.telemetry_metrics.hallucination_prevention_blocks_24h}</span>
              <span className="text-xs font-medium text-muted-foreground">Injections & PII</span>
            </div>
          </div>
        </div>
      )}
      
      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-xl border bg-card shadow-sm">
          <div className="border-b p-6">
            <h3 className="text-lg font-semibold">Live Provider Topology</h3>
            <p className="text-sm text-muted-foreground">Real-time status of LLM circuit breakers</p>
          </div>
          <div className="p-6">
            {metrics?.provider_health.map((p: any, idx: number) => (
              <div key={idx} className="mb-4 flex items-center justify-between last:mb-0">
                <div className="flex items-center gap-3">
                  <Activity className="h-4 w-4 text-muted-foreground" />
                  <span className="font-medium">{p.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`h-2 w-2 rounded-full ${p.circuit_state === 'CLOSED' ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
                  <span className="text-xs text-muted-foreground">{p.circuit_state === 'CLOSED' ? 'HEALTHY' : 'BROKEN'}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-xl border bg-card shadow-sm flex flex-col justify-center items-center p-8 bg-gradient-to-br from-indigo-500/5 to-purple-500/5">
           <ShieldCheck className="h-16 w-16 text-indigo-500/50 mb-4" />
           <h3 className="text-xl font-bold text-center">Zero Data Leakage Assured</h3>
           <p className="text-sm text-muted-foreground text-center mt-2 max-w-xs">All outbound orchestration requests are filtered via the Governance Engine. PII and Enterprise Secrets are masked locally before provider transmission.</p>
        </div>
      </div>
    </div>
  )
}
