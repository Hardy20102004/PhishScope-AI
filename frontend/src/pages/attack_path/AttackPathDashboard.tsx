import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Network, Target, GitMerge, AlertTriangle, ShieldAlert } from 'lucide-react';

export default function AttackPathDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-fuchsia-400">
            <Network size={32} />
            Enterprise Attack Path Simulation
          </h1>
          <p className="text-slate-400 mt-2">Graph-based defensive modeling of trust relationships, network exposure, and critical asset choke points.</p>
        </div>
        <Button className="bg-fuchsia-600 hover:bg-fuchsia-700 text-white shadow-lg shadow-fuchsia-500/20 gap-2">
            <Target size={18} /> Simulate New Campaign
        </Button>
      </div>

      {/* Top Level Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <MetricCard title="Total Nodes Modeled" value="14,204" icon={<Network size={20} className="text-slate-500"/>} />
          <MetricCard title="Edges (Relationships)" value="89,112" icon={<GitMerge size={20} className="text-slate-500"/>} />
          <MetricCard title="Critical Assets Exposed" value="12" icon={<AlertTriangle size={20} className="text-rose-500 animate-pulse"/>} color="text-rose-400" />
          <MetricCard title="Avg Path Complexity" value="3.2 Hops" icon={<ShieldAlert size={20} className="text-amber-500"/>} color="text-amber-400" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Top Exposed Critical Assets */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Most Exposed Critical Assets</h3>
                  <div className="space-y-4">
                      <ExposedAssetRow asset="Production Payments DB" type="AWS RDS" paths={412} complexity={2} />
                      <ExposedAssetRow asset="Domain Controller (DC-01)" type="Server" paths={288} complexity={3} />
                      <ExposedAssetRow asset="Jenkins Build Server" type="Application" paths={194} complexity={4} />
                  </div>
              </CardContent>
          </Card>

          {/* Top Choke Points */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Critical Remediation Choke Points</h3>
                  <div className="space-y-4">
                      <ChokePointRow asset="ServiceAccount_Backup" type="Identity" reduction={120} />
                      <ChokePointRow asset="JUMP_HOST_01" type="Server" reduction={85} />
                      <ChokePointRow asset="VPC_Peering_Prod_Dev" type="Network" reduction={44} />
                  </div>
              </CardContent>
          </Card>

      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, color = "text-slate-200" }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">{title}</h3>
                    {icon}
                </div>
                <div className={`text-3xl font-black ${color}`}>{value}</div>
            </CardContent>
        </Card>
    );
}

function ExposedAssetRow({ asset, type, paths, complexity }: any) {
    return (
        <div className="flex justify-between items-center p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <div className="flex flex-col">
                <span className="text-sm font-bold text-slate-200">{asset}</span>
                <span className="text-[10px] text-fuchsia-400 font-mono uppercase">{type}</span>
            </div>
            <div className="flex gap-4 text-right">
                <div className="flex flex-col">
                    <span className="text-[10px] text-slate-500 uppercase">Viable Paths</span>
                    <span className="text-sm font-bold text-rose-400">{paths}</span>
                </div>
                <div className="flex flex-col">
                    <span className="text-[10px] text-slate-500 uppercase">Min Hops</span>
                    <span className="text-sm font-bold text-amber-400">{complexity}</span>
                </div>
            </div>
        </div>
    );
}

function ChokePointRow({ asset, type, reduction }: any) {
    return (
        <div className="flex justify-between items-center p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <div className="flex flex-col">
                <span className="text-sm font-bold text-slate-200">{asset}</span>
                <span className="text-[10px] text-sky-400 font-mono uppercase">{type}</span>
            </div>
            <div className="flex flex-col text-right">
                <span className="text-[10px] text-slate-500 uppercase">Paths Severed</span>
                <span className="text-sm font-bold text-emerald-400">-{reduction}</span>
            </div>
        </div>
    );
}
