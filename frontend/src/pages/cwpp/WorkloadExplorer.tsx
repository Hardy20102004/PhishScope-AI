import React from 'react';
import { Server, Box, Zap, ShieldAlert, ShieldCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function WorkloadExplorer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Server className="text-indigo-400" />
                    Cloud Workload Explorer
                </h2>
                <p className="text-slate-400 mt-1">Unified inventory of all active VMs, Pods, and Serverless compute instances.</p>
            </div>
            <div className="flex gap-2">
                <input type="text" placeholder="Search workloads (e.g. prod-api)..." className="bg-slate-900 border border-slate-700 rounded px-4 py-2 text-sm text-slate-200 w-64 focus:outline-none focus:border-indigo-500" />
                <Button className="bg-indigo-600 hover:bg-indigo-700 text-white">Filter</Button>
            </div>
        </div>

        <div className="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden">
            <table className="w-full text-left text-sm">
                <thead className="bg-slate-950/50 border-b border-slate-800 text-slate-400 font-bold uppercase text-xs tracking-wider">
                    <tr>
                        <th className="px-6 py-4">Workload Name</th>
                        <th className="px-6 py-4">Type</th>
                        <th className="px-6 py-4">Provider / Region</th>
                        <th className="px-6 py-4">Criticality</th>
                        <th className="px-6 py-4">Runtime Risk</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                    <WorkloadRow name="prod-api-pod-8b4d" type="Kubernetes Pod" provider="AWS (us-east-1)" icon={<Box size={16} />} crit="HIGH" risk="CRITICAL" />
                    <WorkloadRow name="staging-db-vm" type="Virtual Machine" provider="Azure (eastus)" icon={<Server size={16} />} crit="MEDIUM" risk="LOW" />
                    <WorkloadRow name="payment-processor-fn" type="Serverless Function" provider="AWS (eu-central-1)" icon={<Zap size={16} />} crit="CRITICAL" risk="LOW" />
                    <WorkloadRow name="dev-worker-pod-2x" type="Kubernetes Pod" provider="GCP (europe-west1)" icon={<Box size={16} />} crit="LOW" risk="MEDIUM" />
                </tbody>
            </table>
        </div>
    </div>
  );
}

function WorkloadRow({ name, type, provider, icon, crit, risk }: any) {
    let riskIcon = <ShieldCheck size={16} className="text-emerald-400" />;
    let riskColor = "text-emerald-400 font-bold";
    if (risk === 'CRITICAL') {
        riskIcon = <ShieldAlert size={16} className="text-rose-400" />;
        riskColor = "text-rose-400 font-bold";
    } else if (risk === 'MEDIUM') {
        riskIcon = <ShieldAlert size={16} className="text-amber-400" />;
        riskColor = "text-amber-400 font-bold";
    }

    return (
        <tr className="hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4 font-bold text-slate-200">
                <div className="flex items-center gap-2">
                    <span className="text-indigo-400">{icon}</span> {name}
                </div>
            </td>
            <td className="px-6 py-4 text-slate-400">{type}</td>
            <td className="px-6 py-4 text-slate-400 font-mono text-xs">{provider}</td>
            <td className="px-6 py-4">
                <span className={`text-[10px] font-black tracking-widest px-2 py-1 rounded border border-slate-700 bg-slate-800 text-slate-300`}>
                    {crit}
                </span>
            </td>
            <td className="px-6 py-4">
                <div className="flex items-center gap-2">
                    {riskIcon}
                    <span className={riskColor}>{risk}</span>
                </div>
            </td>
        </tr>
    );
}
