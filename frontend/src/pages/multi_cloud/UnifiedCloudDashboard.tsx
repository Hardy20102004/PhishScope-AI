import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Globe, Server, ShieldAlert, Activity } from 'lucide-react';

export default function UnifiedCloudDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-indigo-400">
            <Globe size={32} />
            Enterprise Multi-Cloud Security Intelligence
          </h1>
          <p className="text-slate-400 mt-2">Unified apex view of posture, identity, workloads, data, and threat detection across AWS, Azure, and GCP.</p>
        </div>
        <div className="flex gap-4">
            <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/20 gap-2">
                <Activity size={18} /> Generate Executive Summary
            </Button>
        </div>
      </div>

      {/* Top Posture Area */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <PostureCard title="Enterprise Cloud Risk Score" value="482" subtitle="High Risk" icon={<ShieldAlert size={24} className="text-rose-400 animate-pulse"/>} highlight="rose" />
          <PostureCard title="Total Unified Assets" value="42,198" subtitle="Across 3 Providers" icon={<Server size={24} className="text-slate-400"/>} />
          <PostureCard title="Active Toxic Combinations" value="14" subtitle="Critical Path Risk" icon={<ShieldAlert size={24} className="text-amber-400"/>} highlight="amber" />
          <PostureCard title="Global Compliance (NIST)" value="82%" subtitle="Needs Improvement" icon={<Activity size={24} className="text-blue-400"/>} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Risk by Provider */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Risk Contribution by Provider</h3>
                  <div className="space-y-4">
                      <ProviderRow provider="Amazon Web Services" score={289} percent={60} color="bg-amber-500" />
                      <ProviderRow provider="Microsoft Azure" score={145} percent={30} color="bg-blue-500" />
                      <ProviderRow provider="Google Cloud Platform" score={48} percent={10} color="bg-rose-500" />
                  </div>
              </CardContent>
          </Card>

          {/* Risk by Category */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Risk Contribution by Category</h3>
                  <div className="space-y-4">
                      <CategoryRow name="Cloud Posture (CSPM)" value="High Misconfigurations" trend="up" />
                      <CategoryRow name="Identity & Entitlements (CIEM)" value="Excessive Admin Access" trend="up" />
                      <CategoryRow name="Data Security (DSPM)" value="Unencrypted Storage" trend="down" />
                      <CategoryRow name="Workload Protection (CWPP)" value="Unpatched CVEs" trend="stable" />
                  </div>
              </CardContent>
          </Card>

      </div>
    </div>
  );
}

function PostureCard({ title, value, subtitle, icon, highlight }: any) {
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
                <div className="flex items-baseline gap-2">
                    <div className="text-4xl font-black text-slate-200">{value}</div>
                    {subtitle && <div className="text-xs font-bold text-slate-500">{subtitle}</div>}
                </div>
            </CardContent>
        </Card>
    );
}

function ProviderRow({ provider, score, percent, color }: any) {
    return (
        <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm font-bold text-slate-300">
                <span>{provider}</span>
                <span className="text-slate-500">{score} Risk Points</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
                <div className={`h-2 rounded-full ${color}`} style={{ width: `${percent}%` }}></div>
            </div>
        </div>
    );
}

function CategoryRow({ name, value, trend }: any) {
    let trendColor = "text-slate-500";
    let trendIcon = "−";
    if (trend === 'up') { trendColor = "text-rose-500"; trendIcon = "↑"; }
    if (trend === 'down') { trendColor = "text-emerald-500"; trendIcon = "↓"; }

    return (
        <div className="flex justify-between items-center p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <span className="text-sm font-bold text-slate-300">{name}</span>
            <div className="flex items-center gap-4">
                <span className="text-xs text-slate-400">{value}</span>
                <span className={`font-bold ${trendColor}`}>{trendIcon}</span>
            </div>
        </div>
    );
}
