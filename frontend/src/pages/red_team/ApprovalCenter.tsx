import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ShieldCheck, Clock, Fingerprint, Lock } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function ApprovalCenter() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Lock className="text-emerald-400" />
                Governance & Authorization Gates
            </h2>
            <p className="text-slate-400 mt-1">Cryptographic stakeholder sign-offs required prior to campaign execution.</p>
        </div>

        <div className="max-w-3xl space-y-4 font-mono">
            
            <ApprovalRow 
                role="Chief Information Security Officer (CISO)" 
                status="SIGNED" 
                time="2026-07-28 14:00 UTC"
                hash="a4b9c1d2e3f4"
            />
            
            <ApprovalRow 
                role="Legal Counsel" 
                status="SIGNED" 
                time="2026-07-28 16:30 UTC"
                hash="f9e8d7c6b5a4"
            />
            
            <ApprovalRow 
                role="System Owner (Prod DB)" 
                status="PENDING" 
            />

        </div>
        
        <div className="max-w-3xl mt-8 pt-6 border-t border-slate-800 flex justify-end gap-4">
            <Button variant="outline" className="border-slate-700 bg-slate-800 text-slate-300">Reject & Send Back</Button>
            <Button className="bg-emerald-600 hover:bg-emerald-700 text-white gap-2 shadow-lg shadow-emerald-500/20">
                <Fingerprint size={16}/> Digitally Sign Authorization
            </Button>
        </div>
    </div>
  );
}

function ApprovalRow({ role, status, time, hash }: any) {
    const isSigned = status === 'SIGNED';
    
    return (
        <Card className={`bg-slate-900 border ${isSigned ? 'border-emerald-900/50' : 'border-amber-900/50'}`}>
            <CardContent className="p-4 flex items-center justify-between">
                <div>
                    <h3 className="text-sm font-bold text-slate-200 font-sans">{role}</h3>
                    {isSigned && (
                        <p className="text-[10px] text-slate-500 mt-1 flex items-center gap-1">
                            <Clock size={10} /> {time} | Hash: <span className="text-emerald-500">{hash}</span>
                        </p>
                    )}
                </div>
                
                {isSigned ? (
                    <span className="flex items-center gap-1 text-xs font-bold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded border border-emerald-500/20">
                        <ShieldCheck size={14} /> AUTHORIZED
                    </span>
                ) : (
                    <span className="flex items-center gap-1 text-xs font-bold text-amber-400 bg-amber-500/10 px-3 py-1 rounded border border-amber-500/20 animate-pulse">
                        <Clock size={14} /> AWAITING SIGNATURE
                    </span>
                )}
            </CardContent>
        </Card>
    );
}
