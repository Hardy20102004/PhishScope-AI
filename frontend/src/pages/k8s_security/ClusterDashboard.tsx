import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Hexagon, ShieldAlert, Key, Activity } from 'lucide-react';

export default function ClusterDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-blue-400">
            <Hexagon size={32} />
            Kubernetes Security & Container Runtime Defense
          </h1>
          <p className="text-slate-400 mt-2">Continuous cluster posture, RBAC analysis, and runtime behavioral monitoring.</p>
        </div>
        <div className="flex gap-4">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-500/20 gap-2">
                <Activity size={18} /> View Runtime Stream
            </Button>
        </div>
      </div>

      {/* Top Posture Area */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <PostureCard title="Monitored Clusters" value="14" icon={<Hexagon size={24} className="text-slate-400"/>} />
          <PostureCard title="Over-Privileged Roles (RBAC)" value="8" icon={<Key size={24} className="text-amber-400 animate-pulse"/>} highlight="amber" />
          <PostureCard title="Container Runtime Anomalies" value="3" icon={<ShieldAlert size={24} className="text-rose-400 animate-pulse"/>} highlight="rose" />
          <PostureCard title="CIS K8s Benchmark" value="92%" icon={<Activity size={24} className="text-emerald-400"/>} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Cluster Distribution */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Multi-Cluster Distribution</h3>
                  <div className="space-y-4">
                      <ClusterRow provider="Amazon EKS" count={8} percent={57} color="bg-amber-500" />
                      <ClusterRow provider="Azure AKS" count={4} percent={28} color="bg-blue-500" />
                      <ClusterRow provider="Google GKE" count={2} percent={15} color="bg-rose-500" />
                  </div>
              </CardContent>
          </Card>

          {/* Top Cluster Risks */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                      <h3 className="text-lg font-bold text-slate-200">Highest Risk Clusters</h3>
                      <span className="text-xs font-bold text-slate-400">By Aggregate Score</span>
                  </div>
                  <div className="space-y-4">
                      <RiskRow name="prod-eks-us-east" provider="EKS" risk="CRITICAL" issues={12} />
                      <RiskRow name="staging-aks-core" provider="AKS" risk="HIGH" issues={8} />
                      <RiskRow name="dev-gke-europe" provider="GKE" risk="MEDIUM" issues={3} />
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

function ClusterRow({ provider, count, percent, color }: any) {
    return (
        <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm font-bold text-slate-300">
                <span>{provider}</span>
                <span className="text-slate-500">{count} Clusters</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
                <div className={`h-2 rounded-full ${color}`} style={{ width: `${percent}%` }}></div>
            </div>
        </div>
    );
}

function RiskRow({ name, provider, risk, issues }: any) {
    let riskColor = "text-amber-400 bg-amber-950/30 border-amber-900/50";
    if (risk === 'CRITICAL') riskColor = "text-rose-400 bg-rose-950/30 border-rose-900/50";
    if (risk === 'HIGH') riskColor = "text-orange-400 bg-orange-950/30 border-orange-900/50";

    return (
        <div className="flex flex-col gap-2 p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <div className="flex justify-between items-start">
                <span className="text-sm font-bold text-slate-300">{name} <span className="text-xs text-slate-500 ml-2 font-normal">({provider})</span></span>
                <span className={`text-[10px] font-bold tracking-widest px-2 py-1 rounded border ${riskColor}`}>
                    {risk}
                </span>
            </div>
            <div className="text-xs text-slate-500 font-bold">
                {issues} active issues
            </div>
        </div>
    );
}
