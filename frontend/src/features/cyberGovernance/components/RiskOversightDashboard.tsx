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
        <div className="border rounded-lg bg-secondary/10 p-6 overflow-x-auto">
          <div className="min-w-[600px]">
            <div className="grid grid-cols-5 gap-2 mb-2 text-center text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              <div></div>
              <div>Cyber Risk</div>
              <div>Operational Risk</div>
              <div>Compliance Risk</div>
              <div>Financial Risk</div>
            </div>
            
            <div className="space-y-2">
              {[
                { name: 'Engineering', risks: ['bg-red-500/80', 'bg-amber-500/80', 'bg-emerald-500/80', 'bg-emerald-500/80'] },
                { name: 'Finance', risks: ['bg-emerald-500/80', 'bg-emerald-500/80', 'bg-amber-500/80', 'bg-red-500/80'] },
                { name: 'Operations', risks: ['bg-amber-500/80', 'bg-red-500/80', 'bg-amber-500/80', 'bg-emerald-500/80'] },
                { name: 'HR & Legal', risks: ['bg-emerald-500/80', 'bg-emerald-500/80', 'bg-red-500/80', 'bg-emerald-500/80'] }
              ].map((dept, i) => (
                <div key={i} className="grid grid-cols-5 gap-2 items-center">
                  <div className="text-sm font-medium text-right pr-4 text-foreground">{dept.name}</div>
                  {dept.risks.map((colorClass, j) => (
                    <div 
                      key={j} 
                      className={`h-16 rounded-md ${colorClass} flex items-center justify-center text-white/90 font-medium shadow-sm transition-transform hover:scale-105 cursor-pointer`}
                    >
                      {colorClass.includes('red') ? 'High' : colorClass.includes('amber') ? 'Med' : 'Low'}
                    </div>
                  ))}
                </div>
              ))}
            </div>
            
            <div className="mt-8 flex items-center justify-center space-x-6 text-sm text-muted-foreground">
              <div className="flex items-center"><div className="w-4 h-4 bg-red-500/80 rounded mr-2"></div> High Risk (Immediate Action)</div>
              <div className="flex items-center"><div className="w-4 h-4 bg-amber-500/80 rounded mr-2"></div> Medium Risk (Monitor)</div>
              <div className="flex items-center"><div className="w-4 h-4 bg-emerald-500/80 rounded mr-2"></div> Low Risk (Acceptable)</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
