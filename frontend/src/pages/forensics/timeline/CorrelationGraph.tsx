import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Network, Link2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function CorrelationGraph() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Network className="text-sky-400" />
                Evidence Correlation Map
            </h2>
            <p className="text-slate-400 mt-1">Identifies how disparate artifacts are connected by shared IOCs or causal chains.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <CorrelationBlock 
                type="SHARED_IP" 
                value="203.0.113.5"
                eventA={{ module: "MEMORY", desc: "Outbound beacon from invoice.exe" }}
                eventB={{ module: "CLOUD", desc: "AssumeRole API call" }}
            />
            <CorrelationBlock 
                type="CAUSAL_SPAWN" 
                value="invoice.exe"
                eventA={{ module: "EMAIL", desc: "Attachment received in inbox" }}
                eventB={{ module: "DISK", desc: "File written to Downloads folder" }}
            />
        </div>
    </div>
  );
}

function CorrelationBlock({ type, value, eventA, eventB }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800 relative overflow-hidden">
            {/* Background connection line */}
            <div className="absolute top-1/2 left-0 right-0 h-px bg-slate-800/50 -z-0"></div>
            
            <CardContent className="p-6 relative z-10 flex flex-col items-center">
                
                {/* The Link */}
                <div className="bg-slate-950 border border-slate-700 px-4 py-2 rounded-full flex flex-col items-center mb-6 shadow-xl shadow-slate-950">
                    <span className="text-[10px] text-slate-500 font-bold tracking-wider mb-1 flex items-center gap-1">
                        <Link2 size={10} className="text-sky-400" /> {type}
                    </span>
                    <span className="text-sm font-mono text-sky-400 font-bold">{value}</span>
                </div>

                {/* The Events */}
                <div className="w-full flex justify-between gap-4">
                    <EventNode {...eventA} />
                    <EventNode {...eventB} />
                </div>
            </CardContent>
        </Card>
    );
}

function EventNode({ module, desc }: any) {
    return (
        <div className="flex-1 bg-slate-950 border border-slate-800 p-4 rounded text-center">
            <Badge className="bg-slate-800 text-slate-300 border-slate-700 mb-2">{module}</Badge>
            <p className="text-xs text-slate-400">{desc}</p>
        </div>
    );
}
