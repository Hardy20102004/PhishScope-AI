import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { List, ShieldAlert, Key } from 'lucide-react';

export default function AuditLogViewer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <List className="text-cyan-400" />
                Cloud Audit Logs (IAM)
            </h2>
            <p className="text-slate-400 mt-1">Searchable chronological log of administrative actions, automatically highlighting anomalous IAM behavior.</p>
        </div>

        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-0">
                <div className="grid grid-cols-12 gap-4 p-4 border-b border-slate-800 bg-slate-950/50 text-xs font-bold text-slate-500 tracking-wider">
                    <div className="col-span-2">TIMESTAMP / IP</div>
                    <div className="col-span-3">ACTOR IDENTITY</div>
                    <div className="col-span-3">EVENT NAME / SOURCE</div>
                    <div className="col-span-4">ANOMALY STATUS</div>
                </div>
                
                <div className="divide-y divide-slate-800/50 font-mono text-sm">
                    <AuditRow 
                        time="Jul 27, 2026 14:00:12" 
                        ip="203.0.113.5"
                        actor="arn:aws:iam::12345:user/dev-01" 
                        event="AssumeRole"
                        source="sts.amazonaws.com"
                        isAnomalous={false}
                    />
                    <AuditRow 
                        time="Jul 27, 2026 14:05:01" 
                        ip="203.0.113.5"
                        actor="arn:aws:sts::12345:assumed-role/AdminRole/dev-01" 
                        event="CreateAccessKey"
                        source="iam.amazonaws.com"
                        isAnomalous={true}
                        reason="Long-term credential creation by assumed role from untrusted IP."
                    />
                </div>
            </CardContent>
        </Card>
    </div>
  );
}

function AuditRow({ time, ip, actor, event, source, isAnomalous, reason }: any) {
    return (
        <div className={`grid grid-cols-12 gap-4 p-4 items-center ${isAnomalous ? 'bg-rose-950/20 hover:bg-rose-950/40' : 'hover:bg-slate-800/20'}`}>
            <div className="col-span-2 flex flex-col gap-1">
                <span className="text-slate-400 text-xs">{time}</span>
                <span className="text-slate-500 text-[10px]">{ip}</span>
            </div>
            
            <div className="col-span-3 flex items-center gap-2">
                <Key size={14} className="text-slate-500 shrink-0" />
                <span className={`truncate text-xs ${isAnomalous ? 'text-rose-400' : 'text-slate-300'}`} title={actor}>{actor}</span>
            </div>
            
            <div className="col-span-3 flex flex-col gap-1">
                <span className="font-bold text-slate-200 text-xs">{event}</span>
                <span className="text-slate-500 text-[10px]">{source}</span>
            </div>

            <div className="col-span-4">
                {isAnomalous ? (
                    <div className="flex flex-col">
                        <span className="flex items-center gap-1 text-xs font-bold text-rose-500 mb-1">
                            <ShieldAlert size={12} /> IAM COMPROMISE DETECTED
                        </span>
                        <span className="text-[10px] text-rose-300 leading-tight">{reason}</span>
                    </div>
                ) : (
                    <span className="text-xs text-slate-600">EXPECTED BEHAVIOR</span>
                )}
            </div>
        </div>
    );
}
