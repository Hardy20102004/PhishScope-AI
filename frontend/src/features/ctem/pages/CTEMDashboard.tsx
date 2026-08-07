import { useState, useEffect } from "react"
import { ShieldAlert, AlertTriangle, CheckCircle, Activity, Globe, Server, Database, Key } from "lucide-react"

// Mock data for the dashboard
const mockExposures = [
  { id: "1", type: "EXPOSED_API", name: "Unauthenticated Payment Gateway API", risk: 9.8, status: "OPEN" },
  { id: "2", type: "MISCONFIG", name: "S3 Bucket Publicly Readable (PII Data)", risk: 8.5, status: "OPEN" },
  { id: "3", type: "CVE", name: "Log4j Vulnerability in Billing Service", risk: 9.2, status: "IN_PROGRESS" },
]

export function CTEMDashboard() {
  const [exposures, setExposures] = useState(mockExposures)

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Cloud Exposure Management</h2>
        <div className="flex items-center space-x-2">
          <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 text-sm font-medium">
            Run AI Prioritization
          </button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {/* Metric Cards */}
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Global Risk Score</h3>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold text-destructive">87/100</div>
            <p className="text-xs text-muted-foreground">+5% from last month</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Critical Exposures</h3>
            <ShieldAlert className="h-4 w-4 text-destructive" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground">3 new since yesterday</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Exposed APIs</h3>
            <Globe className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold">4</div>
            <p className="text-xs text-muted-foreground">In Production VPCs</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Remediation Progress</h3>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold">45%</div>
            <p className="text-xs text-muted-foreground">SLA Compliance Rate</p>
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm col-span-4">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="space-y-1">
              <h3 className="font-semibold leading-none tracking-tight">Attack Surface Topography</h3>
              <p className="text-sm text-muted-foreground">Internet-facing assets across multi-cloud.</p>
            </div>
          </div>
          <div className="p-6 pt-0">
            <div className="h-[300px] w-full flex items-center justify-center border-dashed border-2 rounded-md bg-secondary/20">
              <span className="text-muted-foreground text-sm">Attack Surface Map Visualization</span>
            </div>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm col-span-3">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="space-y-1">
              <h3 className="font-semibold leading-none tracking-tight">Top Prioritized Exposures</h3>
              <p className="text-sm text-muted-foreground">Contextualized by business criticality and AI.</p>
            </div>
          </div>
          <div className="p-6 pt-0">
            <div className="space-y-4">
              {exposures.map(exposure => (
                <div key={exposure.id} className="flex items-center justify-between rounded-lg border p-3">
                  <div className="flex items-center space-x-4">
                    <AlertTriangle className="h-5 w-5 text-destructive" />
                    <div>
                      <p className="text-sm font-medium leading-none">{exposure.name}</p>
                      <p className="text-xs text-muted-foreground mt-1">{exposure.type}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-bold text-destructive">{exposure.risk.toFixed(1)}</p>
                    <p className="text-xs text-muted-foreground">Risk Score</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
