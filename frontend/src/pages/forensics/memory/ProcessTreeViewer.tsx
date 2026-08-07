import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ShieldAlert, Terminal, Layers, EyeOff, Activity } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function ProcessTreeViewer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-end mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Layers className="text-fuchsia-400" />
                    Process Tree Analysis (PsTree)
                </h2>
                <p className="text-slate-400 mt-1">Hierarchical visualization of EPROCESS blocks extracted from RAM.</p>
            </div>
            <div className="flex gap-2">
                <Badge variant="outline" className="border-rose-500/50 text-rose-400 bg-rose-500/10"><EyeOff size={14} className="mr-1"/> DKOM Hidden Processes: 1</Badge>
                <Badge variant="outline" className="border-amber-500/50 text-amber-400 bg-amber-500/10"><Activity size={14} className="mr-1"/> Hollowed Processes: 1</Badge>
            </div>
        </div>

        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-6 font-mono text-sm">
                
                <ProcessRow pid={4} ppid={0} name="System" isSuspicious={false} />
                <ProcessRow pid={342} ppid={4} name="smss.exe" indent={1} />
                <ProcessRow pid={612} ppid={342} name="csrss.exe" indent={2} />
                <ProcessRow pid={1408} ppid={612} name="explorer.exe" indent={3} />
                
                {/* Suspicious Sub-Tree */}
                <div className="relative group">
                    <ProcessRow pid={4912} ppid={1408} name="cmd.exe" indent={4} isSuspicious={true} message="Suspicious parent-child relationship (Explorer -> CMD)" />
                    <ProcessRow pid={9091} ppid={4912} name="svchost.exe" indent={5} isCritical={true} message="DKOM Unlinked (Hidden) + Process Hollowing Detected" />
                </div>
                
                <ProcessRow pid={614} ppid={342} name="wininit.exe" indent={2} />
                
            </CardContent>
        </Card>
    </div>
  );
}

function ProcessRow({ pid, ppid, name, indent = 0, isSuspicious, isCritical, message }: any) {
    const pl = indent * 24;
    let colorClass = 'text-slate-300';
    let bgClass = 'hover:bg-slate-800/50';
    let icon = <Terminal size={14} className="text-slate-500" />;
    
    if (isCritical) {
        colorClass = 'text-rose-400 font-bold';
        bgClass = 'bg-rose-950/30 hover:bg-rose-900/30 border-l-2 border-rose-500';
        icon = <EyeOff size={14} className="text-rose-500" />;
    } else if (isSuspicious) {
        colorClass = 'text-amber-400 font-bold';
        bgClass = 'bg-amber-950/20 hover:bg-amber-900/20 border-l-2 border-amber-500';
        icon = <ShieldAlert size={14} className="text-amber-500" />;
    }

    return (
        <div className={`flex items-center justify-between py-2 px-4 rounded ${bgClass} transition-colors group`}>
            <div className="flex items-center gap-3" style={{ paddingLeft: `${pl}px` }}>
                <div className="w-16 text-slate-500 text-xs">PID: {pid}</div>
                {icon}
                <span className={colorClass}>{name}</span>
            </div>
            
            {message && (
                <div className="text-xs bg-slate-950 px-2 py-1 rounded border border-slate-800 text-slate-400">
                    {message}
                </div>
            )}
        </div>
    );
}
