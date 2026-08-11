import { Crosshair } from 'lucide-react';

export function OperationsDashboard() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-xl font-semibold flex items-center">
          <Crosshair className="mr-2 h-5 w-5 text-primary" />
          Cross-Domain Operational Coordination
        </h2>
        <p className="text-sm text-muted-foreground">Unified view of SOC, DFIR, Cloud, and AppSec operations.</p>
      </div>

      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Active Cross-Domain Workflows</h3>
        <div className="space-y-4">
          <div className="bg-secondary/20 p-4 border rounded-lg flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="h-10 w-10 rounded bg-blue-500/20 text-blue-500 flex items-center justify-center font-bold">1</div>
              <div>
                <p className="font-medium text-foreground">Cloud Sec to SOC Handoff</p>
                <p className="text-xs text-muted-foreground">Automated IAM revocation triggered by GuardDuty</p>
              </div>
            </div>
            <span className="px-2 py-1 bg-emerald-500/10 text-emerald-500 text-xs rounded-full font-medium">Active</span>
          </div>
          <div className="bg-secondary/20 p-4 border rounded-lg flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="h-10 w-10 rounded bg-purple-500/20 text-purple-500 flex items-center justify-center font-bold">2</div>
              <div>
                <p className="font-medium text-foreground">DFIR Triage Coordination</p>
                <p className="text-xs text-muted-foreground">Endpoint isolation pending legal approval</p>
              </div>
            </div>
            <span className="px-2 py-1 bg-amber-500/10 text-amber-500 text-xs rounded-full font-medium">Pending</span>
          </div>
          <div className="bg-secondary/20 p-4 border rounded-lg flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="h-10 w-10 rounded bg-emerald-500/20 text-emerald-500 flex items-center justify-center font-bold">3</div>
              <div>
                <p className="font-medium text-foreground">AppSec Vulnerability Sync</p>
                <p className="text-xs text-muted-foreground">Jira tickets synced with critical findings</p>
              </div>
            </div>
            <span className="px-2 py-1 bg-emerald-500/10 text-emerald-500 text-xs rounded-full font-medium">Completed</span>
          </div>
        </div>
      </div>
    </div>
  );
}
