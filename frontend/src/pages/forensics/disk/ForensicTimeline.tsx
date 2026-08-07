import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Clock, Plus, Trash2, Edit3 } from 'lucide-react';

export default function ForensicTimeline() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <div className="border-b border-slate-800 pb-4 mb-8">
            <h1 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Clock className="text-indigo-400" />
                MAC Forensic Timeline
            </h1>
            <p className="text-slate-400 mt-1">Chronological reconstruction of file system activity (Modified, Accessed, Created).</p>
        </div>

        <div className="relative border-l-2 border-slate-800 ml-4 space-y-8 pb-12">
            
            <TimelineEvent 
                date="2026-07-27 14:32:11 UTC"
                action="CREATED"
                file="C:\Temp\malware.exe"
                icon={<Plus size={16} />}
                color="text-emerald-400"
                bg="bg-emerald-500/10"
                borderColor="border-emerald-500/20"
            />
            
            <TimelineEvent 
                date="2026-07-27 15:01:45 UTC"
                action="MODIFIED"
                file="C:\Windows\System32\cmd.exe"
                icon={<Edit3 size={16} />}
                color="text-blue-400"
                bg="bg-blue-500/10"
                borderColor="border-blue-500/20"
            />
            
            <TimelineEvent 
                date="2026-07-28 09:15:22 UTC"
                action="DELETED"
                file="C:\Users\Admin\Desktop\passwords.txt"
                icon={<Trash2 size={16} />}
                color="text-rose-400"
                bg="bg-rose-500/10"
                borderColor="border-rose-500/20"
            />
            
        </div>
    </div>
  );
}

function TimelineEvent({ date, action, file, icon, color, bg, borderColor }: any) {
    const [expanded, setExpanded] = useState(false);
    return (
        <div className="relative pl-8">
            <div className={`absolute -left-[9px] top-1 w-4 h-4 rounded-full border-4 border-slate-950 bg-slate-400`}></div>
            <div className="flex flex-col sm:flex-row sm:items-start gap-4 cursor-pointer group" onClick={() => setExpanded(!expanded)}>
                <div className="w-48 text-xs font-mono text-slate-500 mt-3">{date}</div>
                <Card className={`flex-1 bg-slate-900 border-slate-800 hover:border-slate-700 transition-all ${expanded ? 'border-cyan-500/50 shadow-lg shadow-cyan-500/10' : ''}`}>
                    <CardContent className="p-4 flex flex-col gap-4">
                        <div className="flex items-center gap-4">
                            <div className={`p-2 rounded ${bg} ${color} border ${borderColor}`}>
                                {icon}
                            </div>
                            <div className="flex-1">
                                <span className={`text-xs font-bold tracking-wider ${color}`}>{action}</span>
                                <p className="text-sm font-mono text-slate-300 mt-1">{file}</p>
                            </div>
                        </div>
                        {expanded && (
                            <div className="pt-4 mt-2 border-t border-slate-800/50 text-xs font-mono text-slate-400 space-y-2 animate-in slide-in-from-top-2">
                                <p><span className="text-slate-500">Hash (SHA-256):</span> a1b2c3d4e5f6g7h8i9j0...</p>
                                <p><span className="text-slate-500">Offset:</span> 0x0045B2</p>
                                <p><span className="text-slate-500">User Context:</span> NT AUTHORITY\SYSTEM</p>
                                <p><span className="text-slate-500">MFT Record:</span> {Math.floor(Math.random() * 90000) + 10000}</p>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
