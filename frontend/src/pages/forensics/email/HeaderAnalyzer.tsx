import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ShieldAlert, Server, ArrowDown, Activity } from 'lucide-react';

export default function HeaderAnalyzer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Activity className="text-indigo-400" />
                MIME Header Analysis
            </h2>
            <p className="text-slate-400 mt-1">Chronological MTA routing path and cryptographic authentication results.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Routing Path */}
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold text-slate-200 mb-6 flex items-center gap-2 border-b border-slate-800 pb-2">
                        <Server className="text-sky-400" size={18} /> Routing Path (Received Headers)
                    </h3>
                    
                    <div className="space-y-0 font-mono text-sm">
                        <Hop 
                            num={1} 
                            ip="103.22.1.5" 
                            desc="from unknown by mail.phish.net with SMTP"
                            time="14:00:00 +0000"
                            isSuspicious={true}
                        />
                        <div className="ml-4 h-6 border-l-2 border-dashed border-slate-700"></div>
                        <Hop 
                            num={2} 
                            ip="mail.phish.net" 
                            desc="by mx.company.com with ESMTP"
                            time="14:00:02 +0000"
                        />
                        <div className="ml-4 h-6 border-l-2 border-dashed border-slate-700"></div>
                        <Hop 
                            num={3} 
                            ip="mx.company.com" 
                            desc="by internal-exchange.company.local"
                            time="14:00:05 +0000"
                        />
                    </div>
                </CardContent>
            </Card>

            {/* Auth Results */}
            <Card className="bg-slate-900 border-rose-500/50 shadow-[0_0_20px_rgba(244,63,94,0.1)]">
                <CardContent className="p-6">
                    <h3 className="text-lg font-bold text-rose-400 mb-6 flex items-center gap-2 border-b border-slate-800 pb-2">
                        <ShieldAlert size={18} /> Authentication Results
                    </h3>
                    
                    <div className="space-y-4">
                        <AuthRow 
                            protocol="SPF" 
                            result="FAIL" 
                            details="sender IP is 103.22.1.5, not authorized by microsoft-secure-update.com" 
                        />
                        <AuthRow 
                            protocol="DKIM" 
                            result="FAIL" 
                            details="body hash did not verify (signature mismatch)" 
                        />
                        <AuthRow 
                            protocol="DMARC" 
                            result="FAIL" 
                            details="action=quarantine (domain alignment failed)" 
                        />
                    </div>
                </CardContent>
            </Card>
        </div>
    </div>
  );
}

function Hop({ num, ip, desc, time, isSuspicious }: any) {
    return (
        <div className={`p-3 rounded border ${isSuspicious ? 'bg-rose-950/20 border-rose-500/30' : 'bg-slate-950 border-slate-800'}`}>
            <div className="flex justify-between items-start mb-1">
                <span className={`font-bold ${isSuspicious ? 'text-rose-400' : 'text-sky-400'}`}>Hop {num}: {ip}</span>
                <span className="text-[10px] text-slate-500">{time}</span>
            </div>
            <p className="text-xs text-slate-400">{desc}</p>
        </div>
    );
}

function AuthRow({ protocol, result, details }: any) {
    const isFail = result === 'FAIL';
    return (
        <div className="p-3 bg-slate-950 rounded border border-slate-800 flex flex-col gap-2">
            <div className="flex items-center gap-3">
                <span className="font-bold text-slate-300 w-12">{protocol}</span>
                <span className={`text-xs font-bold px-2 py-1 rounded ${isFail ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'}`}>
                    {result}
                </span>
            </div>
            <p className="text-xs font-mono text-slate-500 pl-[60px]">{details}</p>
        </div>
    );
}
