import { Shield } from 'lucide-react';

export function RiskGovernanceDashboard() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-xl font-semibold flex items-center">
          <Shield className="mr-2 h-5 w-5 text-primary" />
          Aggregated Risk & Governance
        </h2>
        <p className="text-sm text-muted-foreground">Unified compliance and enterprise risk posture.</p>
      </div>

      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Enterprise Compliance Matrix</h3>
        <div className="h-64 flex items-center justify-center border-2 border-dashed border-muted rounded-lg bg-secondary/20">
          <p className="text-muted-foreground text-sm">Aggregated compliance matrix will appear here.</p>
        </div>
      </div>
    </div>
  );
}
