import { TrendingUp } from 'lucide-react';

export function InvestmentDashboard() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-xl font-semibold flex items-center">
          <TrendingUp className="mr-2 h-5 w-5 text-primary" />
          Strategic Investment & ROI
        </h2>
        <p className="text-sm text-muted-foreground">Align cybersecurity investments with business objectives and risk reduction.</p>
      </div>

      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Investment Allocation</h3>
        <div className="h-64 flex items-center justify-center border-2 border-dashed border-muted rounded-lg bg-secondary/20">
          <p className="text-muted-foreground text-sm">Strategic investment ROI charts will appear here.</p>
        </div>
      </div>
    </div>
  );
}
