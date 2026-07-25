import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Users, Server, ShieldCheck, HardDrive } from 'lucide-react';

export default function TenantDashboard() {
  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white mb-2">Tenant Overview</h1>
        <p className="text-slate-400 text-sm">Monitor organization health, license utilization, and system status.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-500/10 text-blue-400 rounded-lg">
                <Users className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">Active Licenses</p>
                <div className="flex items-baseline gap-2">
                  <h3 className="text-2xl font-bold text-white">42</h3>
                  <span className="text-xs text-slate-500">/ 50 seats</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-lg">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">Security Score</p>
                <h3 className="text-2xl font-bold text-white">94%</h3>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-purple-500/10 text-purple-400 rounded-lg">
                <Server className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">API Requests (30d)</p>
                <h3 className="text-2xl font-bold text-white">1.2M</h3>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-amber-500/10 text-amber-400 rounded-lg">
                <HardDrive className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-400">Storage Used</p>
                <div className="flex items-baseline gap-2">
                  <h3 className="text-2xl font-bold text-white">840</h3>
                  <span className="text-xs text-slate-500">GB</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
      
      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <CardTitle>Organization Details</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4 py-3 border-b border-slate-800">
              <div className="text-sm text-slate-400">Organization Name</div>
              <div className="text-sm text-white font-medium">Acme Security Corp</div>
            </div>
            <div className="grid grid-cols-2 gap-4 py-3 border-b border-slate-800">
              <div className="text-sm text-slate-400">Tenant ID</div>
              <div className="text-sm text-slate-300 font-mono">org_8f9a2b3c4d5e</div>
            </div>
            <div className="grid grid-cols-2 gap-4 py-3 border-b border-slate-800">
              <div className="text-sm text-slate-400">Primary Domain</div>
              <div className="text-sm text-white font-medium">acme-security.com</div>
            </div>
            <div className="grid grid-cols-2 gap-4 py-3">
              <div className="text-sm text-slate-400">Data Residency</div>
              <div className="text-sm text-white font-medium flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                US-East (N. Virginia)
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
