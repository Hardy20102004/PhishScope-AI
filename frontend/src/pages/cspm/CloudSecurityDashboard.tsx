import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Cloud, ShieldAlert, CheckCircle, Search, Server } from 'lucide-react';

export default function CloudSecurityDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-sky-400">
            <Cloud size={32} />
            Cloud Security Posture Management (CSPM)
          </h1>
          <p className="text-slate-400 mt-2">Multi-cloud asset discovery, configuration assessment, and continuous compliance monitoring.</p>
        </div>
        <div className="flex gap-4">
            <Button className="bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700">
                Generate Report
            </Button>
            <Button className="bg-sky-600 hover:bg-sky-700 text-white shadow-lg shadow-sky-500/20 gap-2">
                <Search size={18} /> Trigger Full Scan
            </Button>
        </div>
      </div>

      {/* Top Posture Area */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <PostureCard title="Cloud Assets Discovered" value="4,192" icon={<Server size={24} className="text-slate-400"/>} />
          <PostureCard title="Critical Misconfigurations" value="12" icon={<ShieldAlert size={24} className="text-rose-400 animate-pulse"/>} highlight="rose" />
          <PostureCard title="CIS Foundations Compliance" value="88%" icon={<CheckCircle size={24} className="text-emerald-400"/>} />
          <PostureCard title="Publicly Exposed Assets" value="3" icon={<Cloud size={24} className="text-amber-400"/>} highlight="amber" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Multi-Cloud Distribution */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Multi-Cloud Asset Distribution</h3>
                  <div className="space-y-4">
                      <ProviderRow provider="AWS" assetCount={2450} percent={58} color="bg-amber-500" />
                      <ProviderRow provider="Azure" assetCount={1200} percent={28} color="bg-blue-500" />
                      <ProviderRow provider="GCP" assetCount={542} percent={14} color="bg-rose-500" />
                  </div>
              </CardContent>
          </Card>

          {/* Top High-Risk Services */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                      <h3 className="text-lg font-bold text-slate-200">Top Misconfigured Services</h3>
                      <span className="text-xs font-bold text-slate-400">By Severity</span>
                  </div>
                  <div className="space-y-4">
                      <ServiceRiskRow service="S3 Buckets" risk="CRITICAL" count={4} />
                      <ServiceRiskRow service="IAM Roles" risk="HIGH" count={18} />
                      <ServiceRiskRow service="EC2 Instances" risk="MEDIUM" count={45} />
                  </div>
              </CardContent>
          </Card>

      </div>
    </div>
  );
}

function PostureCard({ title, value, icon, highlight }: any) {
    let borderClass = 'border-slate-800';
    if (highlight === 'rose') borderClass = 'border-rose-900/50';
    if (highlight === 'amber') borderClass = 'border-amber-900/50';

    return (
        <Card className={`bg-slate-900 ${borderClass}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider leading-tight">{title}</h3>
                    {icon}
                </div>
                <div className="text-4xl font-black text-slate-200">{value}</div>
            </CardContent>
        </Card>
    );
}

function ProviderRow({ provider, assetCount, percent, color }: any) {
    return (
        <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm font-bold text-slate-300">
                <span>{provider}</span>
                <span className="text-slate-500">{assetCount} Assets</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
                <div className={`h-2 rounded-full ${color}`} style={{ width: `${percent}%` }}></div>
            </div>
        </div>
    );
}

function ServiceRiskRow({ service, risk, count }: any) {
    let riskColor = "text-amber-400 bg-amber-950/30 border-amber-900/50";
    if (risk === 'CRITICAL') riskColor = "text-rose-400 bg-rose-950/30 border-rose-900/50";
    if (risk === 'HIGH') riskColor = "text-orange-400 bg-orange-950/30 border-orange-900/50";

    return (
        <div className="flex justify-between items-center p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <span className="text-sm font-bold text-slate-300">{service}</span>
            <div className="flex items-center gap-4">
                <span className="text-sm font-black text-slate-400">{count}</span>
                <span className={`text-[10px] font-bold tracking-widest px-2 py-1 rounded border ${riskColor}`}>
                    {risk}
                </span>
            </div>
        </div>
    );
}
