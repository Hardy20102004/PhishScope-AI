import { useState } from "react"
import { Shield, Settings, Server } from "lucide-react"

export default function ProviderModelManager() {
  const [models] = useState([
    { id: "gemini-3.1-pro", provider: "Gemini", context: "2M Tokens", cost: "$0.0035 / 1K", status: "Active" },
    { id: "claude-3-5-sonnet", provider: "Claude", context: "200K Tokens", cost: "$0.003 / 1K", status: "Active" },
    { id: "gpt-4o", provider: "OpenAI", context: "128K Tokens", cost: "$0.005 / 1K", status: "Fallback" },
    { id: "ollama-local", provider: "Local Ollama", context: "32K Tokens", cost: "$0.00 (Local)", status: "Air-Gapped" },
    { id: "enterprise-self-hosted", provider: "Enterprise", context: "128K Tokens", cost: "$0.00 (Local)", status: "Active" }
  ])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Provider & Model Registry</h1>
        <p className="text-muted-foreground mt-1">Configure LLM endpoints, token limits, and automated failover hierarchies.</p>
      </div>

      <div className="rounded-xl border bg-card shadow-sm">
        <div className="border-b p-6 flex justify-between items-center">
          <div>
            <h2 className="text-lg font-semibold">Registered AI Models</h2>
            <p className="text-sm text-muted-foreground">Ordered by orchestration routing preference</p>
          </div>
          <button className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground shadow transition-all hover:opacity-90">
            <Server className="h-4 w-4" />
            Add Custom Endpoint
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-muted/50 text-xs uppercase text-muted-foreground">
              <tr>
                <th className="p-4">Model ID</th>
                <th className="p-4">Provider Engine</th>
                <th className="p-4">Context Limit</th>
                <th className="p-4">Base Token Cost</th>
                <th className="p-4">Operational Status</th>
                <th className="p-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {models.map((m) => (
                <tr key={m.id} className="hover:bg-muted/30">
                  <td className="p-4 font-medium">{m.id}</td>
                  <td className="p-4">{m.provider}</td>
                  <td className="p-4">{m.context}</td>
                  <td className="p-4">{m.cost}</td>
                  <td className="p-4">
                    <span className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold bg-emerald-500/10 text-emerald-500">
                      <Shield className="h-3 w-3" />
                      {m.status}
                    </span>
                  </td>
                  <td className="p-4 text-right">
                    <button className="rounded-md p-2 hover:bg-muted text-muted-foreground">
                      <Settings className="h-4 w-4" />
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
