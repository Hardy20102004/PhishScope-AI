import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Target, AlertTriangle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function FindingsDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Target className="text-rose-400" />
                Campaign Findings & Remediation
            </h2>
            <p className="text-slate-400 mt-1">Track identified vulnerabilities and detection gaps mapped to MITRE ATT&CK.</p>
        </div>

        <div className="space-y-4 font-mono">
            <FindingRow 
                title="EDR Bypass via API Unhooking" 
                severity="CRITICAL" 
                tactic="Defense Evasion" 
                technique="T1562.001"
                status="OPEN"
            />
            <FindingRow 
                title="Excessive IAM Permissions on Target Role" 
                severity="HIGH" 
                tactic="Privilege Escalation" 
                technique="T1078.004"
                status="OPEN"
            />
            <FindingRow 
                title="Missing Alert for LSASS Memory Dump" 
                severity="MEDIUM" 
                tactic="Credential Access" 
                technique="T1003.001"
                status="REMEDIATED"
            />
        </div>
    </div>
  );
}

function FindingRow({ title, severity, tactic, technique, status }: any) {
    const isRemediated = status === 'REMEDIATED';
    
    let sevColor = "text-sky-400";
    if (severity === 'CRITICAL') sevColor = "text-rose-500";
    if (severity === 'HIGH') sevColor = "text-orange-500";
    if (severity === 'MEDIUM') sevColor = "text-amber-500";

    return (
        <Card className={`bg-slate-900 border ${isRemediated ? 'border-slate-800' : 'border-rose-900/30'}`}>
            <CardContent className="p-4 grid grid-cols-12 gap-4 items-center">
                
                <div className="col-span-1 flex justify-center">
                    {!isRemediated && <AlertTriangle size={20} className={sevColor} />}
                </div>

                <div className="col-span-5 flex flex-col gap-1">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Finding</span>
                    <span className={`text-sm ${isRemediated ? 'text-slate-500 line-through' : 'text-slate-200'}`}>{title}</span>
                </div>
                
                <div className="col-span-4 flex flex-col gap-2">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">MITRE ATT&CK Mapping</span>
                    <div className="flex gap-2">
                        <Badge className="bg-slate-800 text-slate-300 border-slate-700 font-mono text-[10px]">{tactic}</Badge>
                        <Badge className="bg-slate-800 text-slate-300 border-slate-700 font-mono text-[10px]">{technique}</Badge>
                    </div>
                </div>

                <div className="col-span-2 flex justify-end">
                    <span className={`text-xs font-bold px-2 py-1 rounded ${isRemediated ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-500 border border-rose-500/20'}`}>
                        {status}
                    </span>
                </div>
                
            </CardContent>
        </Card>
    );
}
