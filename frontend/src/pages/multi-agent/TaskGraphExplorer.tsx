import { useState } from "react"
import { GitBranch, Clock, CheckCircle2 } from "lucide-react"

export default function TaskGraphExplorer() {
  const [tasks] = useState([
    { id: "URL-01", agent: "url-analysis-agent", status: "COMPLETED", duration: "1.2s" },
    { id: "EML-01", agent: "email-analysis-agent", status: "COMPLETED", duration: "2.5s" },
    { id: "INT-01", agent: "threat-intel-agent", status: "RUNNING", duration: "4.1s (Dependency: URL-01, EML-01)" },
    { id: "RPT-01", agent: "report-writer-agent", status: "PENDING", duration: "Waiting on INT-01" },
  ])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Execution DAG Explorer</h1>
        <p className="text-muted-foreground mt-1">Visualize multi-agent parallel execution graphs and dependencies.</p>
      </div>

      <div className="rounded-xl border bg-card shadow-sm">
        <div className="border-b p-6 flex justify-between items-center">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <GitBranch className="h-5 w-5 text-indigo-500" />
            Active Investigation: Case #9981-A
          </h2>
          <span className="inline-flex rounded-full bg-indigo-500/10 px-3 py-1 text-sm font-semibold text-indigo-500">
            DAG Running
          </span>
        </div>

        <div className="p-6">
          <div className="space-y-4">
            {tasks.map((t, idx) => (
              <div key={idx} className="flex items-center gap-4 rounded-lg border p-4 hover:border-primary/50 transition-colors">
                {t.status === 'COMPLETED' ? (
                  <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                ) : t.status === 'RUNNING' ? (
                  <Clock className="h-5 w-5 text-amber-500 animate-pulse" />
                ) : (
                  <Clock className="h-5 w-5 text-muted-foreground" />
                )}
                
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <p className="font-semibold text-foreground">{t.id}</p>
                    <span className="text-xs font-mono text-muted-foreground">{t.agent}</span>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">{t.duration}</p>
                </div>
                
                <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full ${
                  t.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-500' :
                  t.status === 'RUNNING' ? 'bg-amber-500/10 text-amber-500' : 'bg-muted text-muted-foreground'
                }`}>
                  {t.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
