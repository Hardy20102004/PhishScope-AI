import { useState } from "react"
import { Trash2, Clock, Layers } from "lucide-react"

export default function ConversationMemoryExplorer() {
  const [sessions] = useState([
    { id: "sess_4021A", tier: "CONVERSATION", created: "12 minutes ago", ttl: "3 Days", turns: 6, status: "Active" },
    { id: "sess_8923F", tier: "CASE_MEMORY", created: "1 hour ago", ttl: "7 Days", turns: 14, status: "Compressed" },
    { id: "sess_1120B", tier: "EVIDENCE_VAULT", created: "4 hours ago", ttl: "30 Days", turns: 22, status: "Active" }
  ])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Multi-Tiered Memory Manager</h1>
        <p className="text-muted-foreground mt-1">Audit active conversation turns, sliding-window compressions, and TTL expirations.</p>
      </div>

      <div className="rounded-xl border bg-card shadow-sm">
        <div className="border-b p-6 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Layers className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-semibold">Active Memory Tier Contexts</h2>
          </div>
          <button className="flex items-center gap-2 rounded-lg bg-destructive/10 px-4 py-2 text-sm font-semibold text-destructive transition-all hover:bg-destructive/20">
            <Trash2 className="h-4 w-4" />
            Purge Expired Data
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-muted/50 text-xs uppercase text-muted-foreground">
              <tr>
                <th className="p-4">Context / Session ID</th>
                <th className="p-4">Memory Tier</th>
                <th className="p-4">Created</th>
                <th className="p-4">Retention TTL</th>
                <th className="p-4">Turn Count</th>
                <th className="p-4">Memory Status</th>
                <th className="p-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {sessions.map((s) => (
                <tr key={s.id} className="hover:bg-muted/30">
                  <td className="p-4 font-medium text-primary">{s.id}</td>
                  <td className="p-4">
                    <span className="inline-flex rounded-md bg-secondary px-2 py-1 text-xs font-semibold text-secondary-foreground">{s.tier}</span>
                  </td>
                  <td className="p-4 text-muted-foreground">{s.created}</td>
                  <td className="p-4 flex items-center gap-1 text-muted-foreground">
                    <Clock className="h-3.5 w-3.5" /> {s.ttl}
                  </td>
                  <td className="p-4 font-semibold">{s.turns} turns</td>
                  <td className="p-4">
                    <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold ${s.status === 'Compressed' ? 'bg-amber-500/10 text-amber-500' : 'bg-emerald-500/10 text-emerald-500'}`}>
                      {s.status}
                    </span>
                  </td>
                  <td className="p-4 text-right">
                    <button className="rounded-md p-2 hover:bg-muted text-muted-foreground hover:text-destructive">
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
