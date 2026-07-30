import { Activity, Server, Database, GitBranch, Cpu, Network } from 'lucide-react';

export function ObservabilityDashboard() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500 max-w-7xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground flex items-center">
          <Activity className="mr-2 h-6 w-6 text-primary" />
          CyberOS Kernel Observability
        </h2>
        <p className="text-muted-foreground mt-1">
          Global platform health, module registry status, and orchestration metrics.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-card border rounded-lg p-5 flex flex-col justify-between shadow-sm">
          <div className="flex justify-between items-start">
            <h3 className="text-sm font-medium text-muted-foreground">Kernel Status</h3>
            <Cpu className="h-4 w-4 text-emerald-500" />
          </div>
          <div className="mt-4">
            <div className="text-3xl font-bold tracking-tight text-emerald-500">ONLINE</div>
            <p className="text-xs text-muted-foreground mt-1">Uptime: 99.999%</p>
          </div>
        </div>
        
        <div className="bg-card border rounded-lg p-5 flex flex-col justify-between shadow-sm">
          <div className="flex justify-between items-start">
            <h3 className="text-sm font-medium text-muted-foreground">Registered Modules</h3>
            <Server className="h-4 w-4 text-primary" />
          </div>
          <div className="mt-4">
            <div className="text-3xl font-bold tracking-tight text-foreground">22 / 22</div>
            <p className="text-xs text-emerald-500 mt-1 flex items-center">
              All systems nominal
            </p>
          </div>
        </div>

        <div className="bg-card border rounded-lg p-5 flex flex-col justify-between shadow-sm">
          <div className="flex justify-between items-start">
            <h3 className="text-sm font-medium text-muted-foreground">Global API Latency</h3>
            <Network className="h-4 w-4 text-amber-500" />
          </div>
          <div className="mt-4">
            <div className="text-3xl font-bold tracking-tight text-foreground">42ms</div>
            <p className="text-xs text-muted-foreground mt-1">Avg response across domains</p>
          </div>
        </div>

        <div className="bg-card border rounded-lg p-5 flex flex-col justify-between shadow-sm">
          <div className="flex justify-between items-start">
            <h3 className="text-sm font-medium text-muted-foreground">Knowledge Graph</h3>
            <GitBranch className="h-4 w-4 text-primary" />
          </div>
          <div className="mt-4">
            <div className="text-3xl font-bold tracking-tight text-foreground">14.2M</div>
            <p className="text-xs text-muted-foreground mt-1">Active nodes and edges</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-card border rounded-lg p-6 shadow-sm">
          <h3 className="text-lg font-medium mb-4 flex items-center">
            <Database className="mr-2 h-5 w-5 text-muted-foreground" />
            Active Module Registry
          </h3>
          <div className="space-y-3">
            {['SOC Fusion', 'DFIR', 'Knowledge Evolution', 'Cyber Command', 'Zero Trust'].map((mod, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-secondary/30 border border-border/50">
                <span className="font-medium text-sm">{mod}</span>
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-500 text-[10px] font-bold tracking-wider">ONLINE</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-card border rounded-lg p-6 shadow-sm flex flex-col">
          <h3 className="text-lg font-medium mb-4 flex items-center">
            <Activity className="mr-2 h-5 w-5 text-muted-foreground" />
            Global Performance Telemetry
          </h3>
          <div className="flex-1 flex items-center justify-center border-2 border-dashed border-muted rounded-lg bg-secondary/10">
            <p className="text-muted-foreground text-sm">Aggregated telemetry stream visualization here.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
