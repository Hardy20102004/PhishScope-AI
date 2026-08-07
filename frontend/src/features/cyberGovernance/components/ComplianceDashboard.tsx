import { CheckSquare } from 'lucide-react';

export function ComplianceDashboard() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-xl font-semibold flex items-center">
          <CheckSquare className="mr-2 h-5 w-5 text-primary" />
          Regulatory Compliance & Readiness
        </h2>
        <p className="text-sm text-muted-foreground">Track adherence to regulatory frameworks and standards.</p>
      </div>

      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Framework Readiness</h3>
        <div className="h-64 flex items-center justify-center border-2 border-dashed border-muted rounded-lg bg-secondary/20">
          <p className="text-muted-foreground text-sm">Compliance framework trackers will appear here.</p>
        </div>
      </div>
    </div>
  );
}
