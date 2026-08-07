import { useState } from "react"
import { ShieldAlert, ThumbsUp, ThumbsDown, UserX } from "lucide-react"

export default function HumanApprovalPanel() {
  const [approvals] = useState([
    { id: "REQ-001", task: "Block 10.0.0.5", agent: "recommendation-agent", severity: "HIGH", conflict: false },
    { id: "REQ-002", task: "Quarantine User Endpoint", agent: "malware-analysis-agent", severity: "CRITICAL", conflict: true, reason: "Agent Threat Intel conflicts with Local Policy Agent (Confidence: 0.62)" }
  ])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Human-in-the-Loop Triage</h1>
        <p className="text-muted-foreground mt-1">Review conflicting agent findings and authorize high-risk containment actions.</p>
      </div>

      <div className="grid gap-6">
        {approvals.map((req, idx) => (
          <div key={idx} className="rounded-xl border bg-card p-6 shadow-sm">
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2">
                  <ShieldAlert className={`h-5 w-5 ${req.severity === 'CRITICAL' ? 'text-rose-500' : 'text-amber-500'}`} />
                  <h2 className="text-lg font-bold text-foreground">{req.task}</h2>
                </div>
                <p className="text-sm font-mono text-muted-foreground mt-2">Requested by: {req.agent}</p>
                
                {req.conflict && (
                  <div className="mt-4 rounded-md bg-rose-500/10 p-3 text-sm text-rose-500 border border-rose-500/20">
                    <strong>Conflict Detected: </strong> {req.reason}
                  </div>
                )}
              </div>
              <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${req.severity === 'CRITICAL' ? 'bg-rose-500/10 text-rose-500' : 'bg-amber-500/10 text-amber-500'}`}>
                {req.severity} RISK
              </span>
            </div>
            
            <div className="mt-6 flex gap-3 border-t pt-4">
              <button className="flex items-center gap-2 rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-600 transition-all">
                <ThumbsUp className="h-4 w-4" /> Approve Action
              </button>
              <button className="flex items-center gap-2 rounded-lg bg-destructive px-4 py-2 text-sm font-semibold text-destructive-foreground hover:bg-destructive/90 transition-all">
                <ThumbsDown className="h-4 w-4" /> Reject Action
              </button>
              <button className="flex items-center gap-2 rounded-lg border bg-background px-4 py-2 text-sm font-semibold hover:bg-muted transition-all">
                <UserX className="h-4 w-4" /> Manual Override
              </button>
            </div>
          </div>
        ))}
        {approvals.length === 0 && (
          <div className="text-center p-12 border rounded-xl text-muted-foreground">
            No pending human approvals.
          </div>
        )}
      </div>
    </div>
  )
}
