import { Activity } from 'lucide-react';

export function RiskOversightDashboard() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-xl font-semibold flex items-center">
          <Activity className="mr-2 h-5 w-5 text-primary" />
          Risk Oversight
        </h2>
        <p className="text-sm text-muted-foreground">Multi-dimensional risk analysis across business and technology domains.</p>
      </div>

      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Enterprise Risk Heatmap</h3>
        <div className="h-96 flex items-center justify-center border-2 border-dashed border-muted rounded-lg bg-secondary/20">
          <p className="text-muted-foreground text-sm">Risk Oversight Heatmap visualization will appear here.</p>
        </div>
      </div>
    </div>
  );
}
