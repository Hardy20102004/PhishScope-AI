import { Card, CardHeader, CardTitle, CardContent } from '../../../components/ui/Card';
import { BarChart3 } from 'lucide-react';
import { Button } from '../../../components/ui/Button';

export default function MetricsExplorer() {
  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white mb-2">Metrics Explorer</h1>
          <p className="text-slate-400 text-sm">Visualize application telemetry and system performance over time.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="border-slate-700">Last 1 Hour</Button>
          <Button variant="outline" className="border-slate-700">Last 24 Hours</Button>
          <Button variant="outline" className="border-slate-700">Last 7 Days</Button>
        </div>
      </div>

      <Card className="bg-slate-900 border-slate-800">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-slate-300 font-medium">Global API Request Latency (P95)</CardTitle>
          <BarChart3 className="w-4 h-4 text-slate-500" />
        </CardHeader>
        <CardContent>
          <div className="h-64 mt-4 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-center">
            {/* Placeholder for Recharts/Chart.js integration */}
            <p className="text-slate-500 text-sm font-mono">[ Timeseries Chart Rendered Here via Grafana/Recharts ]</p>
          </div>
        </CardContent>
      </Card>
      
      <div className="grid grid-cols-2 gap-6">
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-slate-300 font-medium">Active Tenants (DAU)</CardTitle>
            <BarChart3 className="w-4 h-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="h-48 mt-4 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-center">
              <p className="text-slate-500 text-xs font-mono">[ DAU Timeseries ]</p>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-slate-300 font-medium">PostgreSQL CPU %</CardTitle>
            <BarChart3 className="w-4 h-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="h-48 mt-4 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-center">
              <p className="text-slate-500 text-xs font-mono">[ DB CPU Timeseries ]</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
