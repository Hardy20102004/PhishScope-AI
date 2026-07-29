import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Link, Hash, Key, User, Download, FileSearch } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function ChainOfCustodyViewer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Link className="text-amber-500" />
                Immutable Chain of Custody Ledger
            </h2>
            <p className="text-slate-400 mt-1">Cryptographically validated history of evidence acquisition, transfers, and analysis.</p>
        </div>

        {/* Evidence Header */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg mb-8 grid grid-cols-2 md:grid-cols-4 gap-6 font-mono text-sm">
            <div className="flex flex-col">
                <span className="text-slate-500 mb-1">Evidence ID</span>
                <span className="text-slate-300 font-bold">EV-982-A4</span>
            </div>
            <div className="flex flex-col">
                <span className="text-slate-500 mb-1">Source Type</span>
                <span className="text-slate-300">DISK_IMAGE (E01)</span>
            </div>
            <div className="flex flex-col col-span-2">
                <span className="text-slate-500 mb-1 flex items-center gap-1"><Hash size={12}/> Original SHA-256</span>
                <span className="text-amber-400 break-all text-xs">8b5a6c1e9f0d2b3a4c5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c</span>
            </div>
        </div>

        {/* Ledger Timeline */}
        <div className="relative pl-6 border-l-2 border-slate-800 space-y-8 py-4 font-mono">
            <LedgerNode 
                time="Jul 27, 2026 14:00:12 UTC"
                action="INGEST"
                actor="admin@company.com"
                hash="a1b2c3d4..."
                notes="Initial acquisition and hashing."
                icon={<Download size={16} className="text-emerald-400" />}
                color="emerald"
            />
            <LedgerNode 
                time="Jul 27, 2026 14:15:33 UTC"
                action="ANALYSIS"
                actor="system_auto_parser"
                hash="f9e8d7c6..."
                notes="Automated MFT parsing initiated."
                icon={<FileSearch size={16} className="text-sky-400" />}
                color="sky"
            />
            <LedgerNode 
                time="Jul 28, 2026 09:30:00 UTC"
                action="TRANSFER"
                actor="analyst2@company.com"
                hash="b4a3c2d1..."
                notes="Evidence checked out for manual review."
                icon={<User size={16} className="text-amber-400" />}
                color="amber"
            />
        </div>
    </div>
  );
}

function LedgerNode({ time, action, actor, hash, notes, icon, color }: any) {
    const colorClasses = {
        sky: "bg-sky-500/10 text-sky-400 border-sky-500/30",
        emerald: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
        amber: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    }[color as 'sky'|'emerald'|'amber'];

    return (
        <div className="relative">
            <div className={`absolute -left-[35px] top-1 w-4 h-4 rounded-full border-2 border-slate-950 bg-${color}-500 z-10 flex items-center justify-center`}>
                <div className={`w-2 h-2 rounded-full bg-${color}-400`}></div>
            </div>
            
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-4 grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="flex flex-col">
                        <span className="text-[10px] text-slate-500 font-bold uppercase">Timestamp</span>
                        <span className="text-xs text-slate-300">{time}</span>
                    </div>
                    
                    <div className="flex items-center gap-2">
                        {icon}
                        <Badge className={`text-[10px] uppercase tracking-wider ${colorClasses}`}>
                            {action}
                        </Badge>
                    </div>

                    <div className="flex flex-col col-span-2">
                        <span className="text-[10px] text-slate-500 font-bold uppercase flex items-center gap-1"><Key size={10}/> Ledger Hash Validation</span>
                        <div className="flex items-center justify-between">
                            <span className="text-xs text-slate-400">{actor}</span>
                            <span className="text-[10px] text-slate-600 bg-slate-950 px-2 py-1 rounded border border-slate-800">{hash}</span>
                        </div>
                        {notes && <p className="text-xs text-slate-400 font-sans mt-2 pt-2 border-t border-slate-800/50">{notes}</p>}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
