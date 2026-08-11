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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[
            { name: 'SOC 2 Type II', score: 92, color: 'bg-emerald-500' },
            { name: 'ISO 27001', score: 85, color: 'bg-emerald-500' },
            { name: 'NIST CSF', score: 78, color: 'bg-primary' },
            { name: 'GDPR / CCPA', score: 65, color: 'bg-amber-500' }
          ].map((fw, idx) => (
            <div key={idx} className="bg-secondary/30 p-4 rounded-lg border">
              <div className="flex justify-between items-center mb-3">
                <span className="font-medium text-foreground">{fw.name}</span>
                <span className="text-sm font-mono text-muted-foreground">{fw.score}% Compliant</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2 overflow-hidden">
                <div className={`h-full ${fw.color}`} style={{ width: `${fw.score}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
