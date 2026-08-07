import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { List, Mail, HardDrive, Cpu, Cloud } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function ChronologicalExplorer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <List className="text-fuchsia-400" />
                Chronological Explorer
            </h2>
            <p className="text-slate-400 mt-1">An unbroken timeline merging artifacts from distinct forensic sources based on UTC timestamps.</p>
        </div>

        <div className="relative pl-6 border-l-2 border-slate-800 space-y-8 py-4 font-mono">
            <TimelineNode 
                time="T-48h 00m"
                module="EMAIL"
                type="EMAIL_DELIVERY"
                summary="Phishing email 'Invoice Update' delivered to ceo@company.com"
                icon={<Mail size={16} className="text-sky-400" />}
                color="sky"
            />
            <TimelineNode 
                time="T-47h 55m"
                module="DISK"
                type="FILE_CREATION"
                summary="invoice.exe written to C:\Users\ceo\Downloads"
                icon={<HardDrive size={16} className="text-emerald-400" />}
                color="emerald"
            />
            <TimelineNode 
                time="T-47h 54m"
                module="MEMORY"
                type="NETWORK_CONNECTION"
                summary="invoice.exe initiated outbound connection to 203.0.113.5:443"
                icon={<Cpu size={16} className="text-amber-400" />}
                color="amber"
            />
            <TimelineNode 
                time="T-24h 00m"
                module="CLOUD"
                type="IAM_ASSUME_ROLE"
                summary="Role assumed from external malicious IP (203.0.113.5)"
                icon={<Cloud size={16} className="text-rose-400" />}
                color="rose"
            />
        </div>
    </div>
  );
}

function TimelineNode({ time, module, type, summary, icon, color }: any) {
    const colorClasses = {
        sky: "bg-sky-500/10 text-sky-400 border-sky-500/30",
        emerald: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
        amber: "bg-amber-500/10 text-amber-400 border-amber-500/30",
        rose: "bg-rose-500/10 text-rose-400 border-rose-500/30",
    }[color as 'sky'|'emerald'|'amber'|'rose'];

    return (
        <div className="relative">
            <div className={`absolute -left-[35px] top-1 w-4 h-4 rounded-full border-2 border-slate-950 bg-${color}-500 z-10 flex items-center justify-center`}>
                <div className={`w-2 h-2 rounded-full bg-${color}-400`}></div>
            </div>
            
            <Card className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
                <CardContent className="p-4 flex gap-6 items-start">
                    <div className="text-xs text-slate-500 whitespace-nowrap pt-1">
                        {time}
                    </div>
                    
                    <div className="flex-1 space-y-2">
                        <div className="flex items-center gap-2">
                            {icon}
                            <Badge className={`text-[10px] uppercase tracking-wider ${colorClasses}`}>
                                {module}
                            </Badge>
                            <span className="text-xs text-slate-300 font-bold">{type}</span>
                        </div>
                        <p className="text-sm text-slate-400 font-sans">{summary}</p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
