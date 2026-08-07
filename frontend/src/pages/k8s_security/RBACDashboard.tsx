import React from 'react';
import { Key, ShieldAlert, CheckCircle, Network } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function RBACDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Key className="text-amber-400" />
                    Kubernetes RBAC Analysis Matrix
                </h2>
                <p className="text-slate-400 mt-1">Effective privileges calculated from Roles, RoleBindings, and ServiceAccounts.</p>
            </div>
            <div className="flex gap-2">
                <input type="text" placeholder="Filter subjects (e.g. jenkins)..." className="bg-slate-900 border border-slate-700 rounded px-4 py-2 text-sm text-slate-200 w-64 focus:outline-none focus:border-amber-500" />
                <Button className="bg-amber-600 hover:bg-amber-700 text-white">Filter</Button>
            </div>
        </div>

        <div className="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden">
            <table className="w-full text-left text-sm">
                <thead className="bg-slate-950/50 border-b border-slate-800 text-slate-400 font-bold uppercase text-xs tracking-wider">
                    <tr>
                        <th className="px-6 py-4">Subject</th>
                        <th className="px-6 py-4">Type</th>
                        <th className="px-6 py-4">Namespace</th>
                        <th className="px-6 py-4">Effective Permissions (Verbs / Resources)</th>
                        <th className="px-6 py-4">Risk Status</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                    <RBACRow 
                        subject="jenkins-ci-sa" 
                        type="ServiceAccount" 
                        namespace="ci-cd" 
                        perms={{"verbs": ["*"], "resources": ["*"]}} 
                        status="CRITICAL" 
                    />
                    <RBACRow 
                        subject="monitoring-prom" 
                        type="ServiceAccount" 
                        namespace="monitoring" 
                        perms={{"verbs": ["get", "list", "watch"], "resources": ["pods", "nodes"]}} 
                        status="SECURE" 
                    />
                    <RBACRow 
                        subject="system:node" 
                        type="Group" 
                        namespace="-" 
                        perms={{"verbs": ["create"], "resources": ["nodes/status"]}} 
                        status="SECURE" 
                    />
                    <RBACRow 
                        subject="legacy-app-role" 
                        type="ServiceAccount" 
                        namespace="production" 
                        perms={{"verbs": ["get"], "resources": ["secrets"]}} 
                        status="HIGH" 
                    />
                </tbody>
            </table>
        </div>
    </div>
  );
}

function RBACRow({ subject, type, namespace, perms, status }: any) {
    let statusStyle = "text-emerald-400 bg-emerald-950/30 border-emerald-900/50";
    if (status === 'CRITICAL') statusStyle = "text-rose-400 bg-rose-950/30 border-rose-900/50";
    if (status === 'HIGH') statusStyle = "text-amber-400 bg-amber-950/30 border-amber-900/50";

    const verbsStr = perms.verbs.join(", ");
    const resStr = perms.resources.join(", ");

    return (
        <tr className="hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4 font-bold text-slate-200">
                <div className="flex items-center gap-2">
                    <Network size={16} className="text-slate-500" /> {subject}
                </div>
            </td>
            <td className="px-6 py-4 text-slate-400">{type}</td>
            <td className="px-6 py-4 text-slate-400 font-mono text-xs">{namespace}</td>
            <td className="px-6 py-4 font-mono text-xs text-slate-400">
                <span className="text-cyan-400">Verbs:</span> [{verbsStr}] <br/>
                <span className="text-cyan-400">Res:</span> [{resStr}]
            </td>
            <td className="px-6 py-4">
                <span className={`text-[10px] font-black tracking-widest px-2 py-1 rounded border ${statusStyle}`}>
                    {status}
                </span>
            </td>
        </tr>
    );
}
