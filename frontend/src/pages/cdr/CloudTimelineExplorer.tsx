import React from 'react';
import { Clock, Database, Cloud, Box } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export default function CloudTimelineExplorer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Clock className="text-sky-400" />
                    Cloud Telemetry Timeline
                </h2>
                <p className="text-slate-400 mt-1">Unified, chronological view of all normalized events across AWS, Azure, GCP, and Kubernetes.</p>
            </div>
            <div className="flex gap-2">
                <input type="text" placeholder="Search raw telemetry..." className="bg-slate-900 border border-slate-700 rounded px-4 py-2 text-sm text-slate-200 w-64 focus:outline-none focus:border-sky-500" />
            </div>
        </div>

        <Card className="bg-black border-slate-800 font-mono text-sm">
            <CardContent className="p-0">
                <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex justify-between text-xs font-bold text-slate-500 uppercase tracking-widest">
                    <span className="w-48">Timestamp / Provider</span>
                    <span className="w-1/3">Event Source / Name</span>
                    <span>Principal / Resource</span>
                </div>
                
                <div className="divide-y divide-slate-900">
                    
                    <TelemetryRow 
                        time="2026-07-29T10:42:01Z" provider="AWS" icon={<Cloud size={14}/>}
                        source="cloudtrail.amazonaws.com" name="ConsoleLogin"
                        principal="svc_legacy_deploy" resource="-"
                    />
                    
                    <TelemetryRow 
                        time="2026-07-29T10:45:12Z" provider="K8S" icon={<Box size={14}/>}
                        source="eks.audit.k8s.io" name="create pods"
                        principal="svc_legacy_deploy" resource="prod-namespace"
                    />

                    <TelemetryRow 
                        time="2026-07-29T10:47:00Z" provider="AWS" icon={<Database size={14}/>}
                        source="s3.amazonaws.com" name="DeleteBucketPolicy"
                        principal="svc_legacy_deploy" resource="arn:aws:s3:::customer-pii-data"
                        highlight={true}
                    />

                </div>
            </CardContent>
        </Card>
    </div>
  );
}

function TelemetryRow({ time, provider, icon, source, name, principal, resource, highlight }: any) {
    const bg = highlight ? "bg-rose-950/20 border-l-2 border-rose-500" : "hover:bg-slate-900/50";
    
    return (
        <div className={`flex p-4 transition-colors ${bg}`}>
            <div className="w-48 shrink-0 flex flex-col gap-1">
                <span className="text-slate-500 text-xs">{time}</span>
                <span className="text-slate-400 font-bold flex items-center gap-1 text-[10px] uppercase">{icon} {provider}</span>
            </div>
            <div className="w-1/3 shrink-0 flex flex-col gap-1">
                <span className="text-sky-400 font-bold">{name}</span>
                <span className="text-slate-500 text-xs">{source}</span>
            </div>
            <div className="flex flex-col gap-1 text-xs">
                <span className="text-slate-300"><span className="text-slate-600">P:</span> {principal}</span>
                <span className="text-slate-400"><span className="text-slate-600">R:</span> {resource}</span>
            </div>
        </div>
    );
}
