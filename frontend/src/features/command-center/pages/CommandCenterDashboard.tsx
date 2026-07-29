import { useState, useEffect } from "react"
import { Monitor, Activity, ShieldCheck, AlertOctagon, TrendingUp, Cpu, Server, Network, Shield } from "lucide-react"

export function CommandCenterDashboard() {
  const [isPresentationMode, setIsPresentationMode] = useState(false)

  // Toggle full screen for SOC presentation
  const togglePresentation = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.error(`Error attempting to enable fullscreen: ${err.message}`)
      })
      setIsPresentationMode(true)
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen()
        setIsPresentationMode(false)
      }
    }
  }

  return (
    <div className={`flex-1 space-y-4 p-8 pt-6 ${isPresentationMode ? 'bg-background h-screen overflow-y-auto' : ''}`}>
      <div className="flex items-center justify-between space-y-2">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Cloud Security Command Center</h2>
          <p className="text-muted-foreground">Unified Operations & AI Defense Analytics</p>
        </div>
        <div className="flex items-center space-x-2">
          <button 
            onClick={togglePresentation}
            className="bg-secondary text-secondary-foreground px-4 py-2 rounded-md hover:bg-secondary/90 text-sm font-medium flex items-center"
          >
            <Monitor className="mr-2 h-4 w-4" />
            {isPresentationMode ? 'Exit Presentation Mode' : 'SOC Presentation Mode'}
          </button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {/* Metric Cards */}
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Enterprise Cloud Health</h3>
            <Activity className="h-4 w-4 text-emerald-500" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold text-emerald-500">94/100</div>
            <p className="text-xs text-muted-foreground">+2% from last week</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Active Critical Alerts</h3>
            <AlertOctagon className="h-4 w-4 text-destructive" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">Requires immediate review</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Compliance Coverage</h3>
            <ShieldCheck className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold">98.5%</div>
            <p className="text-xs text-muted-foreground">Across all cloud accounts</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Automated Remediations</h3>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold">1,204</div>
            <p className="text-xs text-muted-foreground">Last 30 days</p>
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm col-span-5">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="space-y-1">
              <h3 className="font-semibold leading-none tracking-tight">Cross-Cloud Operations Matrix</h3>
              <p className="text-sm text-muted-foreground">Live feed from CSPM, CWPP, DSPM, and Kubernetes Security.</p>
            </div>
          </div>
          <div className="p-6 pt-0">
            <div className="h-[400px] w-full flex items-center justify-center border-dashed border-2 rounded-md bg-secondary/20">
               <div className="text-center space-y-4">
                 <Network className="h-12 w-12 text-primary/50 mx-auto" />
                 <span className="text-muted-foreground text-sm font-medium">Global Cloud Topology & Threat Vectors</span>
               </div>
            </div>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm col-span-2">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <div className="space-y-1">
              <h3 className="font-semibold leading-none tracking-tight">Human Approval Gates</h3>
              <p className="text-sm text-muted-foreground">Pending environment-changing actions.</p>
            </div>
          </div>
          <div className="p-6 pt-0">
            <div className="space-y-4">
                <div className="flex flex-col space-y-2 rounded-lg border p-3 border-l-4 border-l-amber-500">
                  <div className="flex justify-between">
                    <p className="text-sm font-medium leading-none">Isolate EC2 Instance</p>
                    <span className="text-xs bg-amber-500/20 text-amber-500 px-2 py-0.5 rounded">High Risk</span>
                  </div>
                  <p className="text-xs text-muted-foreground">Action triggered by AI CDR due to suspicious lateral movement.</p>
                  <div className="flex space-x-2 pt-2">
                    <button className="text-xs bg-primary text-primary-foreground px-2 py-1 rounded">Approve</button>
                    <button className="text-xs border px-2 py-1 rounded">Deny</button>
                  </div>
                </div>
                
                <div className="flex flex-col space-y-2 rounded-lg border p-3 border-l-4 border-l-blue-500">
                  <div className="flex justify-between">
                    <p className="text-sm font-medium leading-none">Revoke IAM Role</p>
                    <span className="text-xs bg-blue-500/20 text-blue-500 px-2 py-0.5 rounded">Medium</span>
                  </div>
                  <p className="text-xs text-muted-foreground">Unused CIEM over-privileged role detected.</p>
                  <div className="flex space-x-2 pt-2">
                    <button className="text-xs bg-primary text-primary-foreground px-2 py-1 rounded">Approve</button>
                    <button className="text-xs border px-2 py-1 rounded">Deny</button>
                  </div>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
