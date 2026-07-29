import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Server, Activity, ShieldAlert, Cpu } from 'lucide-react';

export default function WorkloadDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      
      {/* Header */}
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-indigo-400">
            <Cpu size={32} />
            Cloud Workload Protection Platform (CWPP)
          </h1>
          <p className="text-slate-400 mt-2">Continuous runtime visibility, behavioral anomaly detection, and workload protection.</p>
        </div>
        <div className="flex gap-4">
            <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/20 gap-2">
                <Activity size={18} /> View Live Telemetry
            </Button>
        </div>
      </div>

      {/* Top Posture Area */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <PostureCard title="Active Workloads" value="1,842" icon={<Server size={24} className="text-slate-400"/>} />
          <PostureCard title="Runtime Events (24h)" value="4.2M" icon={<Activity size={24} className="text-indigo-400"/>} />
          <PostureCard title="Behavioral Anomalies" value="5" icon={<ShieldAlert size={24} className="text-rose-400 animate-pulse"/>} highlight="rose" />
          <PostureCard title="High Risk Workloads" value="2" icon={<Cpu size={24} className="text-amber-400"/>} highlight="amber" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          
          {/* Workload Distribution */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-slate-200 mb-6 border-b border-slate-800 pb-2">Active Workloads by Type</h3>
                  <div className="space-y-4">
                      <WorkloadRow type="Kubernetes Pods" count={1250} percent={68} color="bg-blue-500" />
                      <WorkloadRow type="Virtual Machines" count={450} percent={24} color="bg-indigo-500" />
                      <WorkloadRow type="Serverless Functions" count={142} percent={8} color="bg-emerald-500" />
                  </div>
              </CardContent>
          </Card>

          {/* Top Anomalies */}
          <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-6">
                  <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-2">
                      <h3 className="text-lg font-bold text-slate-200">Active Behavioral Anomalies</h3>
                      <span className="text-xs font-bold text-slate-400">Live Stream</span>
                  </div>
                  <div className="space-y-4">
                      <AnomalyRow title="Interactive Reverse Shell Detected" workload="prod-api-pod-8b4d" severity="CRITICAL" time="2m ago" />
                      <AnomalyRow title="Unexpected Outbound Connection (Port 4444)" workload="staging-db-vm" severity="HIGH" time="14m ago" />
                      <AnomalyRow title="Crypto-Mining Process Signature (xmrig)" workload="batch-worker-node" severity="CRITICAL" time="1h ago" />
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

function WorkloadRow({ type, count, percent, color }: any) {
    return (
        <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm font-bold text-slate-300">
                <span>{type}</span>
                <span className="text-slate-500">{count} Instances</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
                <div className={`h-2 rounded-full ${color}`} style={{ width: `${percent}%` }}></div>
            </div>
        </div>
    );
}

function AnomalyRow({ title, workload, severity, time }: any) {
    let riskColor = "text-amber-400 bg-amber-950/30 border-amber-900/50";
    if (severity === 'CRITICAL') riskColor = "text-rose-400 bg-rose-950/30 border-rose-900/50";
    if (severity === 'HIGH') riskColor = "text-orange-400 bg-orange-950/30 border-orange-900/50";

    return (
        <div className="flex flex-col gap-2 p-3 bg-slate-950/50 rounded border border-slate-800/50">
            <div className="flex justify-between items-start">
                <span className="text-sm font-bold text-slate-300">{title}</span>
                <span className={`text-[10px] font-bold tracking-widest px-2 py-1 rounded border ${riskColor}`}>
                    {severity}
                </span>
            </div>
            <div className="flex justify-between text-xs text-slate-500">
                <span className="font-mono text-indigo-400">{workload}</span>
                <span>{time}</span>
            </div>
        </div>
    );
}
