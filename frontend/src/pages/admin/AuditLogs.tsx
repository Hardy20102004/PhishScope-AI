import { Card, CardContent } from '../../components/ui/Card';
import { Search, Download, Shield } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';

export default function AuditLogs() {
  const logs = [
    { id: 'al_1', time: '2026-07-25 00:01:23', action: 'USER_LOGIN', user: 'alice@acme.com', ip: '192.168.1.5', resource: 'auth' },
    { id: 'al_2', time: '2026-07-24 23:45:10', action: 'POLICY_UPDATE', user: 'alice@acme.com', ip: '192.168.1.5', resource: 'tenant_settings' },
    { id: 'al_3', time: '2026-07-24 22:10:05', action: 'EVIDENCE_EXPORT', user: 'bob@acme.com', ip: '10.0.0.15', resource: 'case_PHX-902' },
    { id: 'al_4', time: '2026-07-24 21:05:00', action: 'FAILED_LOGIN', user: 'unknown', ip: '14.23.45.67', resource: 'auth' },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white mb-2">Audit & Compliance Logs</h1>
          <p className="text-slate-400 text-sm">Immutable ledger of administrative actions and data access events.</p>
        </div>
        <Button variant="outline" className="flex items-center gap-2 border-slate-700">
          <Download className="w-4 h-4" />
          Export SOC2 Report
        </Button>
      </div>

      <Card className="bg-slate-900 border-slate-800">
        <CardContent className="p-0">
          <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
            <div className="flex gap-4 items-center">
              <div className="relative w-80">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input placeholder="Search logs by action, user, or IP..." className="pl-9 bg-slate-950 border-slate-800" />
              </div>
              <div className="text-sm font-medium text-slate-400 flex items-center gap-2">
                <Shield className="w-4 h-4 text-emerald-500" />
                Tamper-Evident Storage Active
              </div>
            </div>
          </div>

          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-500 text-xs uppercase">
              <tr>
                <th className="px-6 py-4 font-medium">Timestamp (UTC)</th>
                <th className="px-6 py-4 font-medium">Action</th>
                <th className="px-6 py-4 font-medium">User</th>
                <th className="px-6 py-4 font-medium">Resource</th>
                <th className="px-6 py-4 font-medium">IP Address</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-800/20 transition-colors font-mono text-xs">
                  <td className="px-6 py-4 text-slate-400">{log.time}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex px-2 py-1 rounded-sm font-semibold ${
                      log.action.includes('FAILED') ? 'bg-red-500/10 text-red-400' : 'bg-slate-800 text-slate-300'
                    }`}>
                      {log.action}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-white">{log.user}</td>
                  <td className="px-6 py-4 text-slate-400">{log.resource}</td>
                  <td className="px-6 py-4 text-slate-500">{log.ip}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
