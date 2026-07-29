import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Activity, AlertTriangle, Zap } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function DetectionHealthDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Activity className="text-amber-400" />
                Detection Health & Fidelity
            </h2>
            <p className="text-slate-400 mt-1">Identify noisy SIEM/EDR rules causing alert fatigue and requiring tuning.</p>
        </div>

        <div className="space-y-4 font-mono">
            <RuleRow 
                name="Suspicious PowerShell Download Cradle" 
                id="CS-PS-001"
                source="CrowdStrike EDR" 
                tp={12} fp={2} 
                status="HEALTHY"
            />
            <RuleRow 
                name="Excessive LDAP Queries (BloodHound)" 
                id="SPL-AD-042"
                source="Splunk SIEM" 
                tp={1} fp={84} 
                status="NOISY"
            />
            <RuleRow 
                name="Potential Pass-the-Hash (Event 4624)" 
                id="SPL-AD-011"
                source="Splunk SIEM" 
                tp={0} fp={0} 
                status="BROKEN"
            />
        </div>
    </div>
  );
}

function RuleRow({ name, id, source, tp, fp, status }: any) {
    const isNoisy = status === 'NOISY';
    const isBroken = status === 'BROKEN';
    const total = tp + fp;
    const fpRatio = total > 0 ? Math.round((fp / total) * 100) : 0;
    
    let statusColor = "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
    if (isNoisy) statusColor = "bg-amber-500/10 text-amber-400 border-amber-500/30 animate-pulse";
    if (isBroken) statusColor = "bg-rose-500/10 text-rose-400 border-rose-500/30";

    return (
        <Card className={`bg-slate-900 border ${isNoisy ? 'border-amber-900/50' : 'border-slate-800'}`}>
            <CardContent className="p-4 grid grid-cols-12 gap-4 items-center">
                
                <div className="col-span-4 flex flex-col gap-1">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Detection Rule</span>
                    <span className="text-sm text-slate-200">{name}</span>
                    <span className="text-[10px] text-sky-400">{source} | {id}</span>
                </div>
                
                <div className="col-span-2 flex flex-col gap-1 text-center">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Volume</span>
                    <span className="text-sm text-slate-300">{total} Alerts</span>
                </div>

                <div className="col-span-3 flex flex-col gap-1 text-center border-x border-slate-800 px-2">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Fidelity</span>
                    <div className="flex justify-center gap-4 text-xs">
                        <span className="text-emerald-400">TP: {tp}</span>
                        <span className="text-rose-400">FP: {fp}</span>
                    </div>
                </div>

                <div className="col-span-3 flex items-center justify-end gap-4">
                    {isNoisy && (
                        <span className="text-[10px] text-amber-500 font-bold">FP Ratio: {fpRatio}%</span>
                    )}
                    <span className={`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded border ${statusColor}`}>
                        {isNoisy && <Zap size={14} />}
                        {isBroken && <AlertTriangle size={14} />}
                        {status}
                    </span>
                </div>
                
            </CardContent>
        </Card>
    );
}
