import React from 'react';
import { GitMerge, Play, Pause, AlertCircle } from 'lucide-react';

export default function WorkflowDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <GitMerge className="text-sky-400" />
                    Automation Orchestration Engine
                </h2>
                <p className="text-slate-400 mt-1">Real-time status of all governance and remediation workflows.</p>
            </div>
            <div className="flex gap-2">
                <input type="text" placeholder="Search workflow ID..." className="bg-slate-900 border border-slate-700 rounded px-4 py-2 text-sm text-slate-200 w-80 focus:outline-none focus:border-sky-500" />
            </div>
        </div>

        <div className="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden">
            <table className="w-full text-left text-sm">
                <thead className="bg-slate-950/50 border-b border-slate-800 text-slate-400 font-bold uppercase text-xs tracking-wider">
                    <tr>
                        <th className="px-6 py-4">Workflow Name</th>
                        <th className="px-6 py-4">Type</th>
                        <th className="px-6 py-4">Status</th>
                        <th className="px-6 py-4">Created</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                    
                    <WorkflowRow 
                        name="Isolate Compromised Production Namespace" 
                        type="REMEDIATION" 
                        status="PENDING_APPROVAL" 
                        time="16 mins ago" 
                    />
                    
                    <WorkflowRow 
                        name="Deploy Custom VPC Flow Log Policy" 
                        type="POLICY_DEPLOYMENT" 
                        status="EXECUTING" 
                        time="2 mins ago" 
                    />

                    <WorkflowRow 
                        name="Revoke Dormant Admin Tokens" 
                        type="REMEDIATION" 
                        status="COMPLETED" 
                        time="1 hour ago" 
                    />

                    <WorkflowRow 
                        name="Accept Risk: Legacy DB Vulnerability" 
                        type="EXCEPTION_REQUEST" 
                        status="REJECTED" 
                        time="3 hours ago" 
                    />

                </tbody>
            </table>
        </div>
    </div>
  );
}

function WorkflowRow({ name, type, status, time }: any) {
    let statStyle = "text-slate-400 bg-slate-900 border-slate-700";
    let icon = <Pause size={12} />;
    
    if (status === 'PENDING_APPROVAL') {
        statStyle = "text-fuchsia-400 bg-fuchsia-950/30 border-fuchsia-900/50";
        icon = <AlertCircle size={12} />;
    } else if (status === 'EXECUTING') {
        statStyle = "text-sky-400 bg-sky-950/30 border-sky-900/50";
        icon = <Play size={12} className="animate-pulse" />;
    } else if (status === 'COMPLETED') {
        statStyle = "text-emerald-400 bg-emerald-950/30 border-emerald-900/50";
        icon = <Check size={12} />;
    } else if (status === 'REJECTED') {
        statStyle = "text-rose-400 bg-rose-950/30 border-rose-900/50";
        icon = <X size={12} />;
    }

    return (
        <tr className="hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4 font-bold text-slate-200">
                {name}
            </td>
            <td className={`px-6 py-4 text-xs font-bold tracking-widest text-slate-500`}>
                {type}
            </td>
            <td className="px-6 py-4">
                <span className={`flex w-fit items-center gap-1 text-[10px] font-black tracking-widest px-2 py-1 rounded border ${statStyle}`}>
                    {icon} {status}
                </span>
            </td>
            <td className="px-6 py-4 text-xs text-slate-500">
                {time}
            </td>
        </tr>
    );
}
// Stub imports for icon
import { Check, X } from 'lucide-react';
