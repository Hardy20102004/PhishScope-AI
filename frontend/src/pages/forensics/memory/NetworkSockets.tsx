import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Globe, ArrowRight, ShieldAlert, Wifi } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function NetworkSockets() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Wifi className="text-fuchsia-400" />
                Active Memory Sockets (Netscan)
            </h2>
            <p className="text-slate-400 mt-1">TCP/UDP connections extracted from volatile kernel memory structures.</p>
        </div>

        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-0">
                <div className="grid grid-cols-6 gap-4 p-4 border-b border-slate-800 bg-slate-950/50 text-xs font-bold text-slate-500 tracking-wider">
                    <div className="col-span-1">PID / PROCESS</div>
                    <div className="col-span-1">PROTOCOL</div>
                    <div className="col-span-1">LOCAL</div>
                    <div className="col-span-2">REMOTE / THREAT INTEL</div>
                    <div className="col-span-1">STATE</div>
                </div>
                
                <div className="divide-y divide-slate-800/50 font-mono text-sm">
                    <SocketRow 
                        pid={1408} process="explorer.exe" 
                        proto="TCPv4" 
                        local="192.168.1.100:49152" 
                        remote="20.44.11.9:443" 
                        state="ESTABLISHED"
                        intel="Microsoft Azure"
                    />
                    <SocketRow 
                        pid={9091} process="svchost.exe (Hidden)" 
                        proto="TCPv4" 
                        local="192.168.1.100:55112" 
                        remote="103.11.42.19:4444" 
                        state="ESTABLISHED"
                        intel="Known C2 (Cobalt Strike)"
                        isCritical={true}
                    />
                    <SocketRow 
                        pid={4} process="System" 
                        proto="TCPv4" 
                        local="0.0.0.0:445" 
                        remote="0.0.0.0:0" 
                        state="LISTENING"
                    />
                </div>
            </CardContent>
        </Card>
    </div>
  );
}

function SocketRow({ pid, process, proto, local, remote, state, intel, isCritical }: any) {
    return (
        <div className={`grid grid-cols-6 gap-4 p-4 items-center ${isCritical ? 'bg-rose-950/10' : 'hover:bg-slate-800/20'}`}>
            <div className="col-span-1 flex flex-col">
                <span className={isCritical ? 'text-rose-400 font-bold' : 'text-slate-300'}>{pid}</span>
                <span className="text-xs text-slate-500">{process}</span>
            </div>
            <div className="col-span-1 text-slate-400 text-xs">{proto}</div>
            <div className="col-span-1 text-slate-400">{local}</div>
            <div className="col-span-2 flex items-center gap-3">
                <ArrowRight size={14} className="text-slate-600" />
                <div className="flex flex-col">
                    <span className={isCritical ? 'text-rose-400 font-bold' : 'text-emerald-400'}>{remote}</span>
                    {intel && (
                        <div className="flex items-center gap-1 mt-1 text-xs">
                            {isCritical ? <ShieldAlert size={12} className="text-rose-500" /> : <Globe size={12} className="text-slate-500" />}
                            <span className={isCritical ? 'text-rose-400' : 'text-slate-500'}>{intel}</span>
                        </div>
                    )}
                </div>
            </div>
            <div className="col-span-1">
                <Badge variant="outline" className={`bg-slate-950 text-xs ${state === 'ESTABLISHED' ? 'text-blue-400 border-blue-500/30' : 'text-slate-400 border-slate-700'}`}>
                    {state}
                </Badge>
            </div>
        </div>
    );
}
