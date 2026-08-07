import { Card, CardContent } from '../../../components/ui/Card';
import { Search, AlertTriangle, Info, CheckCircle2 } from 'lucide-react';
import { Button } from '../../../components/ui/Button';
import { Input } from '../../../components/ui/Input';

export default function IncidentManager() {
  const incidents = [
    { id: 'INC-2041', title: 'High API Latency on Virustotal Connector', severity: 'CRITICAL', status: 'OPEN', component: 'THREAT_FEED', time: '10 mins ago' },
    { id: 'INC-2040', title: 'Database connection pool approaching limits', severity: 'WARNING', status: 'OPEN', component: 'DATABASE', time: '2 hours ago' },
    { id: 'INC-2039', title: 'Multiple failed logins from Org_B', severity: 'INFO', status: 'RESOLVED', component: 'AUTH', time: '1 day ago' },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white mb-2">Incident Manager</h1>
          <p className="text-slate-400 text-sm">Track and resolve application-level anomalies, outages, and alerts.</p>
        </div>
        <Button className="flex items-center gap-2">
          Create Manual Incident
        </Button>
      </div>

      <Card className="bg-slate-900 border-slate-800">
        <CardContent className="p-0">
          <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
            <div className="relative w-80">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <Input placeholder="Search incidents..." className="pl-9 bg-slate-950 border-slate-800" />
            </div>
            <div className="flex gap-2">
              <Button variant="outline" className="border-slate-700">Filter Status: Open</Button>
            </div>
          </div>

          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-500 text-xs uppercase">
              <tr>
                <th className="px-6 py-4 font-medium">Incident ID</th>
                <th className="px-6 py-4 font-medium">Title</th>
                <th className="px-6 py-4 font-medium">Severity</th>
                <th className="px-6 py-4 font-medium">Component</th>
                <th className="px-6 py-4 font-medium text-right">Age</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {incidents.map((inc) => (
                <tr key={inc.id} className="hover:bg-slate-800/20 transition-colors">
                  <td className="px-6 py-4 font-mono text-slate-400">{inc.id}</td>
                  <td className="px-6 py-4 font-medium text-white">{inc.title}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold ${
                      inc.severity === 'CRITICAL' ? 'bg-red-500/10 text-red-400' :
                      inc.severity === 'WARNING' ? 'bg-amber-500/10 text-amber-400' :
                      'bg-blue-500/10 text-blue-400'
                    }`}>
                      {inc.severity === 'CRITICAL' && <AlertTriangle className="w-3 h-3" />}
                      {inc.severity === 'WARNING' && <AlertTriangle className="w-3 h-3" />}
                      {inc.severity === 'INFO' && <Info className="w-3 h-3" />}
                      {inc.severity}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-slate-400 text-xs">{inc.component}</span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end gap-3 text-slate-500">
                      {inc.status === 'RESOLVED' && <CheckCircle2 className="w-4 h-4 text-emerald-500" />}
                      {inc.time}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
