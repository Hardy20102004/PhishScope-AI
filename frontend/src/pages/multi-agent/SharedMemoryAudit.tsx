import { useState } from "react"
import { Database, Search } from "lucide-react"

export default function SharedMemoryAudit() {
  const [memoryItems] = useState([
    { tier: "WORKING", key: "case_9981_scratchpad", size: "14 KB", updated: "2 mins ago" },
    { tier: "EVIDENCE", key: "hash_fc912_artifact", size: "2.1 MB", updated: "15 mins ago" },
    { tier: "ORGANIZATION", key: "actor_apt_29_profile", size: "45 KB", updated: "3 days ago" },
    { tier: "TEMPORARY", key: "url_sandbox_output", size: "8 KB", updated: "Just now" }
  ])

  return (
    <div className="flex h-full flex-col gap-6 p-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">7-Tier Shared Memory Audit</h1>
        <p className="text-muted-foreground mt-1">Inspect working state, organizational knowledge, and evidence tiers shared between agents.</p>
      </div>

      <div className="rounded-xl border bg-card shadow-sm">
        <div className="border-b p-4 flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input 
              type="text" 
              placeholder="Search memory keys across all tiers..." 
              className="w-full rounded-md border bg-transparent py-2 pl-9 pr-4 text-sm outline-none focus:border-primary"
            />
          </div>
          <select className="rounded-md border bg-transparent px-3 py-2 text-sm outline-none">
            <option>All Tiers</option>
            <option>WORKING</option>
            <option>EVIDENCE</option>
            <option>ORGANIZATION</option>
            <option>TEMPORARY</option>
          </select>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-muted/50 text-xs uppercase text-muted-foreground">
              <tr>
                <th className="p-4">Memory Tier</th>
                <th className="p-4">Key Identifier</th>
                <th className="p-4">Object Size</th>
                <th className="p-4">Last Updated</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {memoryItems.map((item, idx) => (
                <tr key={idx} className="hover:bg-muted/30">
                  <td className="p-4">
                    <span className="inline-flex items-center gap-1.5 rounded bg-primary/10 px-2.5 py-0.5 text-xs font-semibold text-primary">
                      <Database className="h-3 w-3" />
                      {item.tier}
                    </span>
                  </td>
                  <td className="p-4 font-mono text-xs">{item.key}</td>
                  <td className="p-4 text-muted-foreground">{item.size}</td>
                  <td className="p-4 text-muted-foreground">{item.updated}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
