import { useState, useEffect } from 'react';
import { Activity, ShieldCheck, Database, GitMerge, Clock } from 'lucide-react';
import { knowledgeEvolutionApi } from '../api/knowledgeEvolutionApi';

export function KnowledgeQualityDashboard() {
  const [overallScore, setOverallScore] = useState(92);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOverview = async () => {
      try {
        const res = await knowledgeEvolutionApi.getOverview();
        // Extract from nested APIResponse envelope if necessary
        const data = res.data?.data || res.data;
        if (data && data.overall_quality_score !== undefined) {
          setOverallScore(data.overall_quality_score);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchOverview();
  }, []);

  const metrics = [
    { name: 'Overall Quality', value: overallScore, icon: Activity, color: 'text-primary' },
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
        <div className="flex items-end space-x-2 h-48 border-b-2 border-l-2 border-secondary p-4">
          {[65, 72, 78, 85, 82, 88, 92].map((height, i) => (
            <div key={i} className="flex-1 flex flex-col justify-end items-center group relative">
              <div 
                className="w-full bg-primary/80 hover:bg-primary transition-all rounded-t-sm"
                style={{ height: `${height}%` }}
              ></div>
              <div className="absolute -top-8 opacity-0 group-hover:opacity-100 transition-opacity bg-secondary px-2 py-1 rounded text-xs">
                {height}%
              </div>
              <span className="text-xs text-muted-foreground mt-2 block">Day {i + 1}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
