import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Puzzle, ShieldAlert, Key } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function ExtensionAnalyzer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Puzzle className="text-emerald-400" />
                Browser Extension Analyzer
            </h2>
            <p className="text-slate-400 mt-1">Review installed extensions and evaluate their requested permissions to identify malicious side-loading.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ExtensionCard 
                name="uBlock Origin" 
                version="1.54.0" 
                id="cjpalhdlnbpafiamejdnhcphjbkeiagm"
                desc="Finally, an efficient blocker. Easy on CPU and memory."
                perms={["<all_urls>", "storage", "tabs", "webRequest"]}
                isSuspicious={false}
            />
            
            <ExtensionCard 
                name="Free PDF Converter Tool" 
                version="2.1" 
                id="aohfdmjgnbmmghihhfgjkjehmfdjebhi"
                desc="Convert PDF to Word"
                perms={["<all_urls>", "tabs", "cookies", "webRequest", "webRequestBlocking"]}
                isSuspicious={true}
                reason="Requested permissions (cookies, webRequestBlocking) vastly exceed stated functionality. High risk for credential harvesting."
            />
        </div>
    </div>
  );
}

function ExtensionCard({ name, version, id, desc, perms, isSuspicious, reason }: any) {
    return (
        <Card className={`bg-slate-900 border-slate-800 ${isSuspicious ? 'border-t-4 border-t-rose-500 ring-1 ring-rose-500/20 shadow-[0_0_15px_rgba(244,63,94,0.1)]' : 'border-t-4 border-t-slate-700'}`}>
            <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                    <div>
                        <CardTitle className="text-lg flex items-center gap-2">
                            {name} 
                            <span className="text-xs text-slate-500 font-mono font-normal">v{version}</span>
                        </CardTitle>
                        <p className="text-xs text-slate-500 font-mono mt-1">ID: {id}</p>
                    </div>
                    {isSuspicious && <Badge className="bg-rose-500/20 text-rose-400 border-rose-500/30">SUSPICIOUS</Badge>}
                </div>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-slate-300 mb-6">{desc}</p>
                
                {isSuspicious && reason && (
                    <div className="bg-rose-950/50 border border-rose-500/30 p-3 rounded mb-6 flex gap-3 text-sm">
                        <ShieldAlert className="text-rose-500 shrink-0" size={18} />
                        <span className="text-rose-200">{reason}</span>
                    </div>
                )}
                
                <div>
                    <h4 className="text-xs font-bold text-slate-500 mb-2 flex items-center gap-1 uppercase tracking-wider">
                        <Key size={12} /> Manifest Permissions
                    </h4>
                    <div className="flex flex-wrap gap-2">
                        {perms.map((p: string, i: number) => (
                            <span key={i} className={`text-xs px-2 py-1 rounded font-mono ${p === '<all_urls>' || p === 'cookies' ? 'bg-amber-950/50 text-amber-400 border border-amber-500/30' : 'bg-slate-950 text-slate-400 border border-slate-800'}`}>
                                {p}
                            </span>
                        ))}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
