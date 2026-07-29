import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Activity, ShieldCheck, ShieldAlert, Cpu } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function SimulationMonitor() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6 flex justify-between items-end">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Activity className="text-emerald-400" />
                    Active Simulation Monitor
                </h2>
                <p className="text-slate-400 mt-1 font-mono text-sm">Session: SIM-2026-991A | Scenario: Credential Dumping (OS Credential Dumping: T1003)</p>
            </div>
            <Badge className="bg-amber-500/20 text-amber-400 border-amber-500/30 animate-pulse">
                STATUS: RUNNING
            </Badge>
        </div>

        <div className="space-y-4 font-mono">
            <StepRow 
                step="1. Execute benign LSASS memory read" 
                control="CrowdStrike EDR" 
                status="DETECTED" 
                refId="CS-ALERT-881"
            />
            <StepRow 
                step="2. Write dumped credentials to C:\Temp" 
                control="CrowdStrike EDR" 
                status="DETECTED" 
                refId="CS-ALERT-882"
            />
            <StepRow 
                step="3. Exfiltrate over DNS (Benign Payload)" 
                control="Palo Alto NDR" 
                status="MISSED" 
                refId="N/A"
            />
        </div>
    </div>
  );
}

function StepRow({ step, control, status, refId }: any) {
    const isDetected = status === 'DETECTED';
    
    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-4 grid grid-cols-12 gap-4 items-center">
                <div className="col-span-5 flex flex-col gap-1">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Simulation Action</span>
                    <span className="text-sm text-slate-300">{step}</span>
                </div>
                
                <div className="col-span-3 flex flex-col gap-1">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Target Control</span>
                    <span className="text-sm text-slate-400 flex items-center gap-2">
                        <Cpu size={14} className="text-sky-400" /> {control}
                    </span>
                </div>

                <div className="col-span-2">
                    <span className={`flex items-center gap-2 text-xs font-bold px-2 py-1 rounded w-max ${isDetected ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'}`}>
                        {isDetected ? <ShieldCheck size={14} /> : <ShieldAlert size={14} />}
                        {status}
                    </span>
                </div>
                
                <div className="col-span-2 flex flex-col items-end gap-1">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Alert Ref</span>
                    <span className="text-xs text-slate-500">{refId}</span>
                </div>
            </CardContent>
        </Card>
    );
}
