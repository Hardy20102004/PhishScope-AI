import { useState } from "react"
import { Users, Activity, Bot, ShieldCheck } from "lucide-react"

export default function AgentDashboard() {
  const [agents] = useState([
    { id: "investigator-agent", name: "Lead Investigator", status: "ACTIVE", health: "HEALTHY", tasks: 142, capability: "Threat Analysis" },
    { id: "threat-intel-agent", name: "Threat Intelligence", status: "ACTIVE", health: "HEALTHY", tasks: 875, capability: "Threat Analysis" },
    { id: "malware-analysis-agent", name: "Malware Analysis", status: "ACTIVE", health: "DEGRADED", tasks: 212, capability: "Threat Hunting" },
    { id: "email-analysis-agent", name: "Email Forensics", status: "ACTIVE", health: "HEALTHY", tasks: 450, capability: "Threat Analysis" },
    { id: "report-writer-agent", name: "Dossier Synthesizer", status: "ACTIVE", health: "HEALTHY", tasks: 110, capability: "Report Writing" },
  ])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">AI Workforce Dashboard</h1>
        <p className="text-muted-foreground mt-1">Command center for all active autonomous cybersecurity agents.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-xl border bg-card p-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="rounded-full bg-primary/10 p-3">
              <Users className="h-6 w-6 text-primary" />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Active Agents</p>
              <h2 className="text-2xl font-bold">14</h2>
            </div>
          </div>
        </div>
        <div className="rounded-xl border bg-card p-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="rounded-full bg-emerald-500/10 p-3">
              <Activity className="h-6 w-6 text-emerald-500" />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Tasks Completed (24h)</p>
              <h2 className="text-2xl font-bold">1,789</h2>
            </div>
          </div>
        </div>
      </div>

      <div className="rounded-xl border bg-card shadow-sm mt-4">
        <div className="border-b p-6">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <Bot className="h-5 w-5 text-primary" /> Specialized Agent Roster
          </h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-muted/50 text-xs uppercase text-muted-foreground">
              <tr>
                <th className="p-4">Agent Name</th>
                <th className="p-4">Agent ID</th>
                <th className="p-4">Core Capability</th>
                <th className="p-4">Status</th>
                <th className="p-4">Health</th>
                <th className="p-4">Tasks Handled</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {agents.map((a) => (
                <tr key={a.id} className="hover:bg-muted/30">
                  <td className="p-4 font-semibold">{a.name}</td>
                  <td className="p-4 text-muted-foreground font-mono text-xs">{a.id}</td>
                  <td className="p-4">{a.capability}</td>
                  <td className="p-4">
                    <span className="inline-flex rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-semibold text-primary">{a.status}</span>
                  </td>
                  <td className="p-4">
                    <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold ${a.health === 'HEALTHY' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-amber-500/10 text-amber-500'}`}>
                      {a.health === 'HEALTHY' && <ShieldCheck className="h-3 w-3" />}
                      {a.health}
                    </span>
                  </td>
                  <td className="p-4 font-medium">{a.tasks}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
