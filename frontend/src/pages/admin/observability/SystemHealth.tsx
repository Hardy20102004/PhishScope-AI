import { Card, CardHeader, CardTitle, CardContent } from '../../../components/ui/Card';
import { Activity, Clock, Server, AlertTriangle } from 'lucide-react';

export default function SystemHealth() {
  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white mb-2">System Health</h1>
        <p className="text-slate-400 text-sm">Real-time observability of application metrics, database health, and API latency.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-lg">
                <Activity className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">Platform Uptime</p>
                <h3 className="text-2xl font-bold text-white">99.99%</h3>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-500/10 text-blue-400 rounded-lg">
                <Clock className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">P95 Latency</p>
                <div className="flex items-baseline gap-2">
                  <h3 className="text-2xl font-bold text-white">124</h3>
                  <span className="text-xs text-slate-500">ms</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-lg">
                <Server className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">Throughput</p>
                <div className="flex items-baseline gap-2">
                  <h3 className="text-2xl font-bold text-white">4.2k</h3>
                  <span className="text-xs text-slate-500">req/s</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-rose-500/10 text-rose-400 rounded-lg">
                <AlertTriangle className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">Error Rate</p>
                <div className="flex items-baseline gap-2">
                  <h3 className="text-2xl font-bold text-white">0.05%</h3>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
      
      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle>Subsystem Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                <span className="text-sm text-slate-300 font-medium">Core API</span>
              </div>
              <span className="text-sm text-slate-500">Operational</span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                <span className="text-sm text-slate-300 font-medium">PostgreSQL Database</span>
              </div>
              <span className="text-sm text-slate-500">Operational</span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-amber-500"></div>
                <span className="text-sm text-slate-300 font-medium">Threat Intelligence Feeds</span>
              </div>
              <span className="text-sm text-slate-500">Degraded (High Latency)</span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                <span className="text-sm text-slate-300 font-medium">AI Copilot Service</span>
              </div>
              <span className="text-sm text-slate-500">Operational</span>
            </div>
            <div className="flex justify-between items-center py-3">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                <span className="text-sm text-slate-300 font-medium">Celery Workers</span>
              </div>
              <span className="text-sm text-slate-500">Operational</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
