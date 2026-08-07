import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Target, GitMerge } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function PurpleTeamMetrics() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <GitMerge className="text-fuchsia-400" />
                Purple Team Correlation
            </h2>
            <p className="text-slate-400 mt-1">Tracking how Red Team findings and BAS validations are driving Blue Team detection improvements.</p>
        </div>

        <div className="space-y-4 font-mono">
            <CorrelationRow 
                source="Red Team Campaign (SIM-2026-A)" 
                finding="EDR Bypass via API Unhooking (T1562.001)"
                blueTeamAction="Deployed new YARA rule for memory scanning"
                status="VALIDATED"
            />
            <CorrelationRow 
                source="BAS Platform (SIM-991)" 
                finding="DNS Exfiltration Missed (T1048.003)"
                blueTeamAction="Tuning NDR threshold for DNS TXT records"
                status="IN_PROGRESS"
            />
        </div>
    </div>
  );
}

function CorrelationRow({ source, finding, blueTeamAction, status }: any) {
    const isValidated = status === 'VALIDATED';

    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-4 grid grid-cols-12 gap-4 items-center">
                
                <div className="col-span-4 flex flex-col gap-1">
                    <span className="text-[10px] text-fuchsia-400 font-bold uppercase">{source}</span>
                    <span className="text-sm text-slate-300">{finding}</span>
                </div>
                
                <div className="col-span-1 flex justify-center text-slate-600">
                    <GitMerge size={20} />
                </div>

                <div className="col-span-5 flex flex-col gap-1">
                    <span className="text-[10px] text-sky-400 font-bold uppercase">Blue Team Remediation</span>
                    <span className="text-sm text-slate-300">{blueTeamAction}</span>
                </div>

                <div className="col-span-2 flex justify-end">
                    <span className={`text-[10px] font-bold px-2 py-1 rounded border ${isValidated ? 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20' : 'bg-amber-500/10 text-amber-500 border-amber-500/20 animate-pulse'}`}>
                        {status}
                    </span>
                </div>
                
            </CardContent>
        </Card>
    );
}
