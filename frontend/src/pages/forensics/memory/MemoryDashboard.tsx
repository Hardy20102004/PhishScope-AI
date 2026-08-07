import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Cpu, UploadCloud, ShieldAlert, Activity } from 'lucide-react';

export default function MemoryDashboard() {
  return (
    <div className="p-8 space-y-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3 text-fuchsia-400">
            <Cpu size={32} />
            Memory Forensics
          </h1>
          <p className="text-slate-400 mt-2">Ingest and analyze volatile memory dumps (RAM) for hidden rootkits, injected processes, and active sockets.</p>
        </div>
        <Button className="bg-fuchsia-600 hover:bg-fuchsia-700 text-white shadow-lg shadow-fuchsia-500/20 gap-2">
            <UploadCloud size={18} /> Upload RAM Dump
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <DumpCard 
              filename="DESKTOP-HR05-MEM.vmem" 
              profile="Win10x64_19041" 
              size="16 GB" 
              status="ANALYZED"
              threats={2}
          />
          <DumpCard 
              filename="SRV-DB01-CRASH.dmp" 
              profile="Linux_CentOS_7" 
              size="64 GB" 
              status="PARSING"
              threats={0}
          />
      </div>
    </div>
  );
}

function DumpCard({ filename, profile, size, status, threats }: any) {
    const isAnalyzed = status === 'ANALYZED';
    const hasThreats = threats > 0;
    
    return (
        <Card className={`bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors ${hasThreats ? 'border-t-4 border-t-rose-500' : isAnalyzed ? 'border-t-4 border-t-emerald-500' : 'border-t-4 border-t-fuchsia-500'}`}>
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                        <Cpu size={20} className="text-slate-400" />
                        <h3 className="text-lg font-bold text-slate-200 truncate" title={filename}>{filename}</h3>
                    </div>
                </div>
                
                <div className="space-y-3 mb-6 font-mono text-sm">
                    <div className="flex justify-between">
                        <span className="text-slate-500">OS Profile</span>
                        <span className="text-slate-300">{profile}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-slate-500">RAM Size</span>
                        <span className="text-slate-300">{size}</span>
                    </div>
                </div>

                <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                    <span className={`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded ${hasThreats ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-fuchsia-500/10 text-fuchsia-400 border border-fuchsia-500/20'}`}>
                        {hasThreats ? <ShieldAlert size={12} /> : <Activity size={12} />}
                        {hasThreats ? `${threats} ANOMALIES` : status}
                    </span>
                    <Button variant="outline" className="text-xs h-8 border-slate-700 bg-slate-800 hover:bg-slate-700">View PsList</Button>
                </div>
            </CardContent>
        </Card>
    );
}
