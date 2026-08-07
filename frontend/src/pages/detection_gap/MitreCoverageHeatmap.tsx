import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Grid, ZoomIn } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function MitreCoverageHeatmap() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Grid className="text-cyan-400" />
                    MITRE ATT&CK Coverage Heatmap
                </h2>
                <p className="text-slate-400 mt-1">Visual representation of detection rule coverage across the attack lifecycle.</p>
            </div>
            <Button variant="outline" className="bg-slate-900 border-slate-700 text-slate-300 gap-2">
                <ZoomIn size={16} /> Expand Matrix
            </Button>
        </div>

        {/* Mock Matrix Visualization */}
        <div className="grid grid-cols-5 gap-4 overflow-x-auto pb-4">
            
            <TacticColumn 
                name="Initial Access" 
                techniques={[
                    { id: "T1566", name: "Phishing", status: "HIGH" },
                    { id: "T1190", name: "Exploit Public-Facing App", status: "MED" },
                    { id: "T1078", name: "Valid Accounts", status: "LOW" },
                ]}
            />

            <TacticColumn 
                name="Execution" 
                techniques={[
                    { id: "T1059", name: "Command and Scripting", status: "HIGH" },
                    { id: "T1204", name: "User Execution", status: "HIGH" },
                    { id: "T1047", name: "WMI", status: "LOW" },
                ]}
            />

            <TacticColumn 
                name="Persistence" 
                techniques={[
                    { id: "T1098", name: "Account Manipulation", status: "MED" },
                    { id: "T1543", name: "Create or Modify System Process", status: "LOW" },
                    { id: "T1136", name: "Create Account", status: "HIGH" },
                ]}
            />

            <TacticColumn 
                name="Defense Evasion" 
                techniques={[
                    { id: "T1562", name: "Impair Defenses", status: "NONE" },
                    { id: "T1070", name: "Indicator Removal", status: "NONE" },
                    { id: "T1218", name: "System Binary Proxy Execution", status: "MED" },
                ]}
            />
            
            <TacticColumn 
                name="Exfiltration" 
                techniques={[
                    { id: "T1048", name: "Exfiltration Over Alt Protocol", status: "NONE" },
                    { id: "T1567", name: "Exfiltration Over Web Service", status: "LOW" },
                ]}
            />
        </div>
    </div>
  );
}

function TacticColumn({ name, techniques }: any) {
    return (
        <div className="flex flex-col gap-2 min-w-[200px]">
            <div className="bg-slate-900 border-b-2 border-cyan-500/50 p-3 text-center rounded-t">
                <span className="text-sm font-bold text-slate-200">{name}</span>
            </div>
            
            {techniques.map((t: any, i: number) => {
                let bg = "bg-emerald-950/40 border-emerald-900/50";
                if (t.status === 'MED') bg = "bg-amber-950/40 border-amber-900/50";
                if (t.status === 'LOW') bg = "bg-rose-950/40 border-rose-900/50";
                if (t.status === 'NONE') bg = "bg-rose-900/80 border-rose-500 animate-pulse";

                return (
                    <div key={i} className={`p-3 border rounded text-center cursor-pointer transition-colors hover:brightness-110 ${bg}`}>
                        <div className="text-[10px] font-mono text-slate-400 mb-1">{t.id}</div>
                        <div className="text-xs font-bold text-slate-200">{t.name}</div>
                    </div>
                )
            })}
        </div>
    );
}
