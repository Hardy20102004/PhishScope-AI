import { useState } from "react"
import { Lock, FileText, CheckCircle } from "lucide-react"

export default function AIObservabilityAudit() {
  const [logs] = useState([
    { id: "REQ-9011A", time: "Just now", model: "claude-3-5-sonnet", capability: "Threat Analysis", status: "SUCCESS", latency: "612ms", hmac: "3f8a00bc91a4e211..." },
    { id: "REQ-9010F", time: "5 mins ago", model: "gemini-3.1-pro", capability: "Evidence Explanation", status: "SUCCESS", latency: "520ms", hmac: "9b1c28fa4e311059..." },
    { id: "REQ-9009B", time: "12 mins ago", model: "PolicyEngine-V1", capability: "Security Guard", status: "POLICY_VIOLATION", latency: "4ms", hmac: "88aa14cc67bf0012..." }
  ])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">AI Governance & Audit Ledger</h1>
          <p className="text-muted-foreground mt-1">AES-256 GCM encrypted AI inference telemetry with immutable HMAC SHA-256 signature chaining.</p>
        </div>
        <div className="flex items-center gap-2 rounded-full border bg-emerald-500/10 px-4 py-2 text-sm font-semibold text-emerald-500 shadow-sm">
          <CheckCircle className="h-4 w-4" />
          NIST AI RMF Compliant
        </div>
      </div>

      <div className="rounded-xl border bg-card shadow-sm">
        <div className="border-b p-6">
          <h2 className="text-lg font-semibold">Cryptographic Inference Audit Trail</h2>
          <p className="text-sm text-muted-foreground">Zero-data-leakage enterprise auditing log for prompt analysis and compliance review</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-muted/50 text-xs uppercase text-muted-foreground">
              <tr>
                <th className="p-4">Request ID</th>
                <th className="p-4">Timestamp</th>
                <th className="p-4">Executed Model</th>
                <th className="p-4">Capability Directive</th>
                <th className="p-4">Latency</th>
                <th className="p-4">Execution Status</th>
                <th className="p-4">HMAC Integrity Signature</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {logs.map((l) => (
                <tr key={l.id} className="hover:bg-muted/30">
                  <td className="p-4 font-medium flex items-center gap-2">
                    <FileText className="h-4 w-4 text-primary" />
                    {l.id}
                  </td>
                  <td className="p-4 text-muted-foreground">{l.time}</td>
                  <td className="p-4 font-semibold text-foreground">{l.model}</td>
                  <td className="p-4">{l.capability}</td>
                  <td className="p-4 text-muted-foreground">{l.latency}</td>
                  <td className="p-4">
                    <span className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-semibold ${l.status === 'SUCCESS' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-rose-500/10 text-rose-500'}`}>
                      {l.status}
                    </span>
                  </td>
                  <td className="p-4 font-mono text-xs text-muted-foreground flex items-center gap-2">
                    <Lock className="h-3.5 w-3.5 text-amber-500" />
                    {l.hmac}
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
