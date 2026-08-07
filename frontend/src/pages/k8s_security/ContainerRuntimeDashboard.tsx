import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Activity, Terminal, Container, Crosshair } from 'lucide-react';

export default function ContainerRuntimeDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Container className="text-sky-400" />
                Container Runtime Defense Stream
            </h2>
            <p className="text-slate-400 mt-1">Live eBPF-driven stream of container lifecycle and process execution anomalies.</p>
        </div>

        <Card className="bg-black border-slate-800 font-mono text-sm">
            <CardContent className="p-0">
                <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex justify-between text-xs font-bold text-slate-500 uppercase tracking-widest">
                    <span>Timestamp</span>
                    <span>Container ID / Pod</span>
                    <span>Event Type / Details</span>
                </div>
                
                <div className="divide-y divide-slate-900">
                    
                    <EventRow 
                        time="10:45:12.301" 
                        container="d9f3a1b (nginx-prod-x2)"
                        type="CONTAINER_START" 
                        icon={<Activity size={14} className="text-emerald-400"/>}
                        details="Container spawned successfully." 
                    />
                    
                    <EventRow 
                        time="10:45:15.912" 
                        container="d9f3a1b (nginx-prod-x2)"
                        type="PROCESS_START" 
                        icon={<Terminal size={14} className="text-slate-400"/>}
                        details="/usr/sbin/nginx -g daemon off;" 
                    />

                    {/* Anomalous Event */}
                    <div className="flex gap-4 p-4 hover:bg-slate-900/50 transition-colors bg-rose-950/20 border-l-2 border-rose-500">
                        <div className="text-slate-500 shrink-0 w-24">10:48:19.441</div>
                        <div className="text-rose-400 font-bold shrink-0 w-48 flex items-center gap-2">
                            <Container size={14} /> a1b2c3d (jenkins-ci-master)
                        </div>
                        <div>
                            <div className="text-rose-400 font-bold flex items-center gap-2 mb-1">
                                <Terminal size={14} /> PRIVILEGED_EXEC_ANOMALY
                            </div>
                            <div className="text-rose-300 break-all">
                                apt-get install -y nmap
                            </div>
                            <div className="mt-2 text-xs text-rose-400/80 bg-rose-950/50 px-2 py-1 rounded inline-block border border-rose-900/50">
                                <Crosshair size={10} className="inline mr-1"/> Action: Blocked by Runtime Policy (Immutable RootFS)
                            </div>
                        </div>
                    </div>

                    <EventRow 
                        time="10:48:20.100" 
                        container="a1b2c3d (jenkins-ci-master)"
                        type="CONTAINER_CRASH" 
                        icon={<Activity size={14} className="text-amber-400"/>}
                        details="Exit Code 1 (OOMKilled: False)" 
                    />

                </div>
            </CardContent>
        </Card>
    </div>
  );
}

function EventRow({ time, container, type, icon, details }: any) {
    return (
        <div className="flex gap-4 p-4 hover:bg-slate-900/50 transition-colors">
            <div className="text-slate-600 shrink-0 w-24">{time}</div>
            <div className="text-slate-400 shrink-0 w-48 font-bold flex items-center gap-2">
                <Container size={14} className="text-slate-600" /> {container}
            </div>
            <div>
                <div className="text-slate-300 font-bold flex items-center gap-2 mb-1">
                    {icon} {type}
                </div>
                <div className="text-slate-500 break-all">
                    {details}
                </div>
            </div>
        </div>
    );
}
