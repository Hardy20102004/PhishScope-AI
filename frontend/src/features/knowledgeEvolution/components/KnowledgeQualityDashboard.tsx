import { Activity, ShieldCheck, Database, GitMerge, Clock } from 'lucide-react';

export function KnowledgeQualityDashboard() {
  const metrics = [
    { name: 'Overall Quality', value: 92, icon: Activity, color: 'text-primary' },
    { name: 'Coverage', value: 88, icon: Database, color: 'text-blue-500' },
    { name: 'Consistency', value: 96, icon: ShieldCheck, color: 'text-emerald-500' },
    { name: 'Relationship Quality', value: 85, icon: GitMerge, color: 'text-purple-500' },
    { name: 'Freshness', value: 98, icon: Clock, color: 'text-amber-500' },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-xl font-semibold flex items-center">
          <Activity className="mr-2 h-5 w-5 text-primary" />
          Knowledge Quality Metrics
        </h2>
        <p className="text-sm text-muted-foreground">Monitor the health and accuracy of the Knowledge Graph.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {metrics.map((metric) => (
          <div key={metric.name} className="bg-card border rounded-lg p-5">
            <div className="flex justify-between items-start mb-4">
              <div className={`p-2 rounded-lg bg-secondary ${metric.color}`}>
                <metric.icon className="h-5 w-5" />
              </div>
            </div>
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-1">{metric.name}</h3>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold tracking-tight text-foreground">{metric.value}</span>
                <span className="text-sm text-muted-foreground">/ 100</span>
              </div>
            </div>
            <div className="mt-4 w-full h-1.5 bg-secondary rounded-full overflow-hidden">
              <div className={`h-full ${metric.value > 90 ? 'bg-emerald-500' : metric.value > 80 ? 'bg-primary' : 'bg-amber-500'}`} style={{ width: `${metric.value}%` }}></div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-card border rounded-lg p-6">
        <h3 className="text-lg font-medium mb-4">Quality Trends</h3>
        <div className="h-64 flex items-center justify-center border-2 border-dashed border-muted rounded-lg bg-secondary/20">
          <p className="text-muted-foreground text-sm">Quality trend visualization will appear here.</p>
        </div>
      </div>
    </div>
  );
}
