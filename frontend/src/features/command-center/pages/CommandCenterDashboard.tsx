import { useState, useEffect } from "react"
import { Monitor, Activity, ShieldCheck, AlertOctagon, TrendingUp, Cpu, Server, Network, Shield, X, Cloud } from "lucide-react"

export function CommandCenterDashboard() {
  const [isPresentationMode, setIsPresentationMode] = useState(false)
  const [isTopologyOpen, setIsTopologyOpen] = useState(false)
  const [healthScore, setHealthScore] = useState(94)
  const [remediations, setRemediations] = useState(1204)
  const [activeAlerts, setActiveAlerts] = useState(3)
  const [pendingApprovals, setPendingApprovals] = useState([
    {
      id: 1,
      title: "Isolate EC2 Instance",
      risk: "High Risk",
      riskColor: "amber",
      description: "Action triggered by AI CDR due to suspicious lateral movement."
    },
    {
      id: 2,
      title: "Revoke IAM Role",
      risk: "Medium",
      riskColor: "blue",
      description: "Unused CIEM over-privileged role detected."
    }
  ])

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

  const handleAction = (id: number) => {
    setPendingApprovals(prev => prev.filter(item => item.id !== id))
  }

  // Simulate Real-time Sync
  useEffect(() => {
    const interval = setInterval(() => {
      setHealthScore(prev => prev > 90 ? prev - Math.floor(Math.random() * 2) : prev + Math.floor(Math.random() * 3));
      setRemediations(prev => prev + Math.floor(Math.random() * 2));
      setActiveAlerts(prev => Math.random() > 0.8 ? (prev > 0 ? prev - 1 : 1) : (Math.random() > 0.9 ? prev + 1 : prev));
    }, 3500);
    return () => clearInterval(interval);
  }, []);

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
            <Activity className="h-4 w-4 text-emerald-500 animate-pulse" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold text-emerald-500 transition-all">{healthScore}/100</div>
            <p className="text-xs text-muted-foreground">+2% from last week</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 className="tracking-tight text-sm font-medium">Active Critical Alerts</h3>
            <AlertOctagon className={`h-4 w-4 ${activeAlerts > 0 ? 'text-destructive animate-pulse' : 'text-muted-foreground'}`} />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold transition-all">{activeAlerts}</div>
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
            <TrendingUp className="h-4 w-4 text-emerald-500" />
          </div>
          <div className="p-6 pt-0">
            <div className="text-2xl font-bold transition-all">{remediations.toLocaleString()}</div>
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
            <div className="w-full border rounded-md bg-background overflow-hidden">
              <table className="w-full text-sm text-left">
                <thead className="bg-secondary/50 text-muted-foreground border-b">
                  <tr>
                    <th className="px-4 py-3 font-medium">Environment</th>
                    <th className="px-4 py-3 font-medium text-center">CSPM</th>
                    <th className="px-4 py-3 font-medium text-center">CWPP</th>
                    <th className="px-4 py-3 font-medium text-center">DSPM</th>
                    <th className="px-4 py-3 font-medium text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  <tr className="hover:bg-muted/50 transition-colors">
                    <td className="px-4 py-3 flex items-center gap-2 font-medium"><Server className="w-4 h-4 text-amber-500" /> AWS Production</td>
                    <td className="px-4 py-3"><ShieldCheck className="w-4 h-4 text-emerald-500 mx-auto" /></td>
                    <td className="px-4 py-3"><ShieldCheck className="w-4 h-4 text-emerald-500 mx-auto" /></td>
                    <td className="px-4 py-3"><AlertOctagon className="w-4 h-4 text-amber-500 mx-auto" /></td>
                    <td className="px-4 py-3 text-center"><span className="text-xs font-medium px-2 py-1 rounded bg-amber-500/10 text-amber-500">Warning</span></td>
                  </tr>
                  <tr className="hover:bg-muted/50 transition-colors">
                    <td className="px-4 py-3 flex items-center gap-2 font-medium"><Network className="w-4 h-4 text-blue-500" /> Azure Corp</td>
                    <td className="px-4 py-3"><ShieldCheck className="w-4 h-4 text-emerald-500 mx-auto" /></td>
                    <td className="px-4 py-3"><ShieldCheck className="w-4 h-4 text-emerald-500 mx-auto" /></td>
                    <td className="px-4 py-3"><ShieldCheck className="w-4 h-4 text-emerald-500 mx-auto" /></td>
                    <td className="px-4 py-3 text-center"><span className="text-xs font-medium px-2 py-1 rounded bg-emerald-500/10 text-emerald-500">Healthy</span></td>
                  </tr>
                  <tr className="hover:bg-muted/50 transition-colors">
                    <td className="px-4 py-3 flex items-center gap-2 font-medium"><Server className="w-4 h-4 text-destructive" /> GCP DataLake</td>
                    <td className="px-4 py-3"><AlertOctagon className="w-4 h-4 text-destructive mx-auto" /></td>
                    <td className="px-4 py-3"><ShieldCheck className="w-4 h-4 text-emerald-500 mx-auto" /></td>
                    <td className="px-4 py-3"><AlertOctagon className="w-4 h-4 text-destructive mx-auto" /></td>
                    <td className="px-4 py-3 text-center"><span className="text-xs font-medium px-2 py-1 rounded bg-destructive/10 text-destructive">Critical</span></td>
                  </tr>
                  <tr className="hover:bg-muted/50 transition-colors">
                    <td className="px-4 py-3 flex items-center gap-2 font-medium"><Cpu className="w-4 h-4 text-purple-500" /> K8s Clusters</td>
                    <td className="px-4 py-3"><ShieldCheck className="w-4 h-4 text-emerald-500 mx-auto" /></td>
                    <td className="px-4 py-3"><ShieldCheck className="w-4 h-4 text-emerald-500 mx-auto" /></td>
                    <td className="px-4 py-3"><ShieldCheck className="w-4 h-4 text-emerald-500 mx-auto" /></td>
                    <td className="px-4 py-3 text-center"><span className="text-xs font-medium px-2 py-1 rounded bg-emerald-500/10 text-emerald-500">Healthy</span></td>
                  </tr>
                </tbody>
              </table>
              <div className="bg-secondary/30 p-4 border-t flex justify-between items-center">
                <div className="text-sm text-muted-foreground flex items-center gap-2">
                  <div className="relative flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                  </div>
                  Real-time sync active
                </div>
                <div onClick={() => setIsTopologyOpen(true)} className="text-sm font-medium text-primary cursor-pointer hover:underline">View Full Topologies</div>
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
                {pendingApprovals.length === 0 ? (
                  <div className="text-sm text-muted-foreground text-center py-4">No pending approvals.</div>
                ) : (
                  pendingApprovals.map(approval => (
                    <div key={approval.id} className={`flex flex-col space-y-2 rounded-lg border p-3 border-l-4 ${approval.riskColor === 'amber' ? 'border-l-amber-500' : 'border-l-blue-500'}`}>
                      <div className="flex justify-between">
                        <p className="text-sm font-medium leading-none">{approval.title}</p>
                        <span className={`text-xs px-2 py-0.5 rounded ${approval.riskColor === 'amber' ? 'bg-amber-500/20 text-amber-500' : 'bg-blue-500/20 text-blue-500'}`}>{approval.risk}</span>
                      </div>
                      <p className="text-xs text-muted-foreground">{approval.description}</p>
                      <div className="flex space-x-2 pt-2">
                        <button onClick={() => handleAction(approval.id)} className="text-xs bg-primary text-primary-foreground px-2 py-1 rounded">Approve</button>
                        <button onClick={() => handleAction(approval.id)} className="text-xs border px-2 py-1 rounded hover:bg-secondary">Deny</button>
                      </div>
                    </div>
                  ))
                )}
            </div>
          </div>
        </div>
      </div>

      {/* Full Topologies Modal */}
      {isTopologyOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-md">
          <div className="relative w-11/12 max-w-5xl bg-card border rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="p-6 border-b bg-muted/30 flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-bold flex items-center gap-2"><Cloud className="text-blue-500" /> Multi-Cloud Network Topology</h2>
                <p className="text-sm text-muted-foreground">Live visualization of your active hybrid-cloud assets and endpoints.</p>
              </div>
              <button onClick={() => setIsTopologyOpen(false)} className="p-2 hover:bg-secondary rounded-full transition-colors">
                <X className="w-5 h-5 text-muted-foreground" />
              </button>
            </div>
            
            <div className="p-8 grid grid-cols-1 md:grid-cols-3 gap-6 h-[60vh] overflow-y-auto">
              {/* AWS Node */}
              <div className="border border-amber-500/30 bg-amber-500/5 rounded-xl p-6 relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-amber-400 to-amber-600"></div>
                <h3 className="text-lg font-bold flex items-center gap-2 mb-4"><Server className="text-amber-500" /> AWS Production (us-east-1)</h3>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm border-b pb-2"><span className="text-muted-foreground">EC2 Instances</span><span className="font-mono">1,402</span></div>
                  <div className="flex justify-between text-sm border-b pb-2"><span className="text-muted-foreground">S3 Buckets</span><span className="font-mono">89</span></div>
                  <div className="flex justify-between text-sm border-b pb-2"><span className="text-muted-foreground">IAM Roles</span><span className="font-mono text-amber-500">2 Over-privileged</span></div>
                  <div className="flex justify-between text-sm"><span className="text-muted-foreground">VPC Flow</span><span className="text-emerald-500 flex items-center gap-1"><Activity className="w-3 h-3" /> Active</span></div>
                </div>
              </div>

              {/* Azure Node */}
              <div className="border border-blue-500/30 bg-blue-500/5 rounded-xl p-6 relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-400 to-blue-600"></div>
                <h3 className="text-lg font-bold flex items-center gap-2 mb-4"><Network className="text-blue-500" /> Azure Corp (eastus)</h3>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm border-b pb-2"><span className="text-muted-foreground">Virtual Machines</span><span className="font-mono">450</span></div>
                  <div className="flex justify-between text-sm border-b pb-2"><span className="text-muted-foreground">Blob Storage</span><span className="font-mono">34</span></div>
                  <div className="flex justify-between text-sm border-b pb-2"><span className="text-muted-foreground">Entra ID Sync</span><span className="text-emerald-500 font-medium">Healthy</span></div>
                  <div className="flex justify-between text-sm"><span className="text-muted-foreground">NSG Rules</span><span className="font-mono">12,045</span></div>
                </div>
              </div>

              {/* GCP Node */}
              <div className="border border-destructive/30 bg-destructive/5 rounded-xl p-6 relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-400 to-red-600"></div>
                <h3 className="text-lg font-bold flex items-center gap-2 mb-4"><Server className="text-destructive" /> GCP DataLake (us-central1)</h3>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm border-b pb-2"><span className="text-muted-foreground">Compute Engines</span><span className="font-mono">890</span></div>
                  <div className="flex justify-between text-sm border-b pb-2"><span className="text-muted-foreground">BigQuery Datasets</span><span className="font-mono text-destructive font-bold">1 Publicly Exposed</span></div>
                  <div className="flex justify-between text-sm border-b pb-2"><span className="text-muted-foreground">Cloud Storage</span><span className="font-mono">12</span></div>
                  <div className="flex justify-between text-sm"><span className="text-muted-foreground">KMS Keys</span><span className="font-mono">45</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
