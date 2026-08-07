import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Box, Layers, ShieldAlert } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function NamespaceExplorer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Layers className="text-purple-400" />
                    Kubernetes Namespace Explorer
                </h2>
                <p className="text-slate-400 mt-1">Topology view of workloads, network policies, and aggregate risk by Namespace.</p>
            </div>
            <div className="flex gap-2">
                <select className="bg-slate-900 border border-slate-700 rounded px-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-purple-500">
                    <option>Cluster: prod-eks-us-east</option>
                    <option>Cluster: staging-aks-core</option>
                </select>
                <Button className="bg-purple-600 hover:bg-purple-700 text-white">Refresh</Button>
            </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            
            <NamespaceCard 
                name="kube-system" 
                pods={24} 
                policies="Enforced" 
                risk="LOW" 
            />

            <NamespaceCard 
                name="production" 
                pods={142} 
                policies="Enforced" 
                risk="MEDIUM" 
                warnings={["Missing Resource Quotas", "3 Pods running as root"]}
            />

            <NamespaceCard 
                name="ci-cd" 
                pods={12} 
                policies="None" 
                risk="CRITICAL" 
                warnings={["Jenkins SA is cluster-admin", "No Network Policies", "Unrestricted Egress"]}
            />

            <NamespaceCard 
                name="monitoring" 
                pods={8} 
                policies="Partial" 
                risk="LOW" 
            />

        </div>
    </div>
  );
}

function NamespaceCard({ name, pods, policies, risk, warnings = [] }: any) {
    let riskBorder = "border-slate-800";
    if (risk === 'CRITICAL') riskBorder = "border-rose-900/50";
    if (risk === 'HIGH') riskBorder = "border-amber-900/50";
    
    let riskColor = "text-emerald-400";
    if (risk === 'CRITICAL') riskColor = "text-rose-400";
    if (risk === 'HIGH') riskColor = "text-orange-400";
    if (risk === 'MEDIUM') riskColor = "text-amber-400";

    return (
        <Card className={`bg-slate-900 ${riskBorder} hover:border-purple-500/50 transition-colors cursor-pointer`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-center mb-6">
                    <h3 className="text-xl font-bold text-slate-200 flex items-center gap-2">
                        <Layers size={20} className="text-purple-400" /> {name}
                    </h3>
                    <span className={`text-[10px] font-black tracking-widest px-2 py-1 rounded border border-slate-800 bg-slate-950 ${riskColor}`}>
                        {risk} RISK
                    </span>
                </div>
                
                <div className="flex justify-between text-sm text-slate-400 mb-4 border-b border-slate-800 pb-4">
                    <div className="flex flex-col">
                        <span className="text-xs uppercase font-bold text-slate-500 mb-1">Active Pods</span>
                        <span className="font-mono text-slate-200">{pods}</span>
                    </div>
                    <div className="flex flex-col">
                        <span className="text-xs uppercase font-bold text-slate-500 mb-1">Network Policies</span>
                        <span className="font-mono text-slate-200">{policies}</span>
                    </div>
                </div>

                {warnings.length > 0 && (
                    <div className="space-y-2">
                        <span className="text-xs font-bold text-rose-400 flex items-center gap-1">
                            <ShieldAlert size={12} /> Active Issues
                        </span>
                        {warnings.map((w: str, i: number) => (
                            <div key={i} className="text-xs text-slate-400 bg-rose-950/20 px-2 py-1 rounded border border-rose-900/30">
                                {w}
                            </div>
                        ))}
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
