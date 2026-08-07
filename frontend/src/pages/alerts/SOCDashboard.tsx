import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle, Clock, Activity, ShieldAlert, CheckCircle } from 'lucide-react';
import apiClient from '@/api/client';

export default function SOCDashboard() {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    // In production, use a proper query hook like React Query
    apiClient.get('/alerts/dashboard/analytics').then((res) => {
      setMetrics(res.data);
    }).catch(console.error);
  }, []);

  if (!metrics) {
    return <div className="flex items-center justify-center h-full text-white">Loading SOC Analytics...</div>;
  }

  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500">
            Enterprise SOC Dashboard
          </h1>
          <p className="text-slate-400 mt-2">Real-time alert volume and analyst metrics</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Active Alerts"
          value={metrics.active_alerts}
          icon={<Activity className="text-blue-400" />}
          trend="+12% from yesterday"
        />
        <MetricCard
          title="Critical Threats"
          value={metrics.critical_alerts}
          icon={<AlertTriangle className="text-red-500" />}
          trend="-2% from yesterday"
          alert
        />
        <MetricCard
          title="Mean Time To Acknowledge"
          value={`${metrics.mtta_minutes}m`}
          icon={<Clock className="text-yellow-400" />}
          trend="Stable"
        />
        <MetricCard
          title="Mean Time To Resolve"
          value={`${metrics.mttr_minutes}m`}
          icon={<CheckCircle className="text-green-400" />}
          trend="-15% from last week"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        <Card className="bg-slate-900 border-slate-800 backdrop-blur-xl">
          <CardHeader>
            <CardTitle className="text-slate-200 flex items-center gap-2">
              <ShieldAlert size={20} />
              Priority Distribution
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(metrics.priority_distribution).map(([priority, count]) => (
                <div key={priority} className="flex items-center justify-between">
                  <Badge variant="outline" className={`
                    ${priority === 'CRITICAL' ? 'border-red-500 text-red-400' : ''}
                    ${priority === 'HIGH' ? 'border-orange-500 text-orange-400' : ''}
                    ${priority === 'MEDIUM' ? 'border-yellow-500 text-yellow-400' : ''}
                    ${priority === 'LOW' ? 'border-green-500 text-green-400' : ''}
                  `}>
                    {priority}
                  </Badge>
                  <span className="text-slate-300 font-mono">{String(count)}</span>
                </div>
              ))}
              {Object.keys(metrics.priority_distribution).length === 0 && (
                <div className="text-slate-500 text-center py-4">No data available</div>
              )}
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800 backdrop-blur-xl">
          <CardHeader>
            <CardTitle className="text-slate-200">Alert Sources</CardTitle>
          </CardHeader>
          <CardContent>
             <div className="space-y-4">
              {Object.entries(metrics.source_distribution).map(([source, count]) => (
                <div key={source} className="flex items-center justify-between">
                  <span className="text-slate-300">{source}</span>
                  <span className="text-slate-300 font-mono">{String(count)}</span>
                </div>
              ))}
              {Object.keys(metrics.source_distribution).length === 0 && (
                <div className="text-slate-500 text-center py-4">No data available</div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, trend, alert = false }: any) {
  return (
    <Card className={`bg-slate-900 border-slate-800 hover:bg-slate-800/80 transition-all duration-300 ${alert ? 'shadow-[0_0_15px_rgba(239,68,68,0.15)] border-red-500/30' : ''}`}>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium text-slate-400">
          {title}
        </CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold text-slate-100">{value}</div>
        <p className={`text-xs mt-2 ${trend.startsWith('+') ? 'text-rose-400' : 'text-emerald-400'}`}>
          {trend}
        </p>
      </CardContent>
    </Card>
  );
}
