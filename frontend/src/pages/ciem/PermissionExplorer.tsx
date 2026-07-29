import React from 'react';
import { Key, ShieldAlert, Network, Server } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function PermissionExplorer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Network className="text-emerald-400" />
                    Effective Permission Matrix
                </h2>
                <p className="text-slate-400 mt-1">Calculated "Who can do What" across AWS, Azure, and GCP resources.</p>
            </div>
            <div className="flex gap-2">
                <input type="text" placeholder="Search resources (e.g. s3:bucket)..." className="bg-slate-900 border border-slate-700 rounded px-4 py-2 text-sm text-slate-200 w-64 focus:outline-none focus:border-emerald-500" />
                <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">Filter</Button>
            </div>
        </div>

        <div className="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden">
            <table className="w-full text-left text-sm">
                <thead className="bg-slate-950/50 border-b border-slate-800 text-slate-400 font-bold uppercase text-xs tracking-wider">
                    <tr>
                        <th className="px-6 py-4">Identity (Principal)</th>
                        <th className="px-6 py-4">Resource Target</th>
                        <th className="px-6 py-4">Effective Action (Permission)</th>
                        <th className="px-6 py-4">Access Type</th>
                        <th className="px-6 py-4">Risk Context</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                    
                    <PermissionRow 
                        identity="alice.smith@corp.com" 
                        resource="arn:aws:s3:::customer-pii-data" 
                        action="s3:GetObject" 
                        type="READ" 
                        risk="SECURE" 
                    />
                    
                    <PermissionRow 
                        identity="svc_legacy_deploy" 
                        resource="arn:aws:iam::123456789012:role/*" 
                        action="iam:PassRole, iam:CreateRole" 
                        type="ADMIN / DESTRUCTIVE" 
                        risk="CRITICAL"
                        riskMsg="Privilege Escalation Vector"
                    />

                    <PermissionRow 
                        identity="AzureAdmins (Group)" 
                        resource="Subscription: Prod-Core" 
                        action="Microsoft.Authorization/roleAssignments/write" 
                        type="ADMIN" 
                        risk="HIGH"
                        riskMsg="Dormant assignment (90+ days)"
                    />

                    <PermissionRow 
                        identity="GCP_Data_Pipeline_SA" 
                        resource="projects/data-warehouse/datasets/*" 
                        action="bigquery.tables.updateData" 
                        type="WRITE" 
                        risk="MEDIUM"
                        riskMsg="Over-broad wildcard target"
                    />

                </tbody>
            </table>
        </div>
    </div>
  );
}

function PermissionRow({ identity, resource, action, type, risk, riskMsg }: any) {
    let riskStyle = "text-emerald-400 bg-emerald-950/30 border-emerald-900/50";
    if (risk === 'CRITICAL') riskStyle = "text-rose-400 bg-rose-950/30 border-rose-900/50";
    if (risk === 'HIGH') riskStyle = "text-amber-400 bg-amber-950/30 border-amber-900/50";
    if (risk === 'MEDIUM') riskStyle = "text-orange-400 bg-orange-950/30 border-orange-900/50";

    return (
        <tr className="hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4 font-bold text-slate-200">
                <div className="flex items-center gap-2">
                    <Key size={16} className="text-slate-500" /> {identity}
                </div>
            </td>
            <td className="px-6 py-4 text-slate-400 font-mono text-xs">
                <div className="flex items-center gap-2">
                    <Server size={14} className="text-slate-500" /> {resource}
                </div>
            </td>
            <td className="px-6 py-4 font-mono text-xs text-sky-400">
                {action}
            </td>
            <td className="px-6 py-4 text-xs font-bold text-slate-300">
                {type}
            </td>
            <td className="px-6 py-4">
                <div className="flex flex-col gap-1 items-start">
                    <span className={`text-[10px] font-black tracking-widest px-2 py-1 rounded border ${riskStyle}`}>
                        {risk}
                    </span>
                    {riskMsg && <span className="text-xs text-slate-500 mt-1">{riskMsg}</span>}
                </div>
            </td>
        </tr>
    );
}
