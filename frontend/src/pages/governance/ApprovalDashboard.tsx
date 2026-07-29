import React from 'react';
import { PenTool, Check, X, ShieldAlert } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function ApprovalDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <PenTool className="text-fuchsia-400" />
                    Human-in-the-Loop Approvals
                </h2>
                <p className="text-slate-400 mt-1">Review and authorize pending automated remediation workflows. Destructive actions require CISO sign-off.</p>
            </div>
        </div>

        <div className="grid grid-cols-1 gap-6">
            
            <Card className="bg-slate-900 border-fuchsia-900/50">
                <CardContent className="p-6">
                    <div className="flex justify-between items-start mb-6 border-b border-slate-800 pb-4">
                        <div>
                            <div className="flex items-center gap-2 mb-2">
                                <span className="text-[10px] font-black tracking-widest px-2 py-1 rounded border border-fuchsia-900/50 bg-fuchsia-950/30 text-fuchsia-400">PENDING YOUR APPROVAL (CISO ROLE)</span>
                            </div>
                            <h3 className="text-lg font-bold text-slate-200 flex items-center gap-2">
                                <ShieldAlert className="text-rose-400" /> Isolate Compromised Production Namespace
                            </h3>
                        </div>
                        <div className="text-right">
                            <div className="text-sm text-slate-400">Workflow ID</div>
                            <div className="font-mono text-xs text-slate-500">wf-98a7b6c5d4</div>
                        </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-8 mb-6">
                        <div>
                            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Proposed Automation Steps</h4>
                            <ul className="space-y-2 text-sm text-slate-300">
                                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span> Apply NetworkPolicy (DenyAll) to `prod-namespace`</li>
                                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span> Revoke all bound ServiceAccount tokens</li>
                                <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-sky-500"></span> Trigger Forensic Snapshot of affected pods</li>
                            </ul>
                        </div>
                        
                        <div>
                            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Approval Chain Status</h4>
                            <div className="space-y-2">
                                <ApprovalChainNode role="L1_SOC_ANALYST" status="APPROVED" user="john.doe" time="14 mins ago" />
                                <ApprovalChainNode role="L2_INCIDENT_RESPONDER" status="APPROVED" user="sarah.smith" time="2 mins ago" />
                                <ApprovalChainNode role="CISO" status="PENDING" user="Current User" time="-" active={true} />
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-4 justify-end border-t border-slate-800 pt-4">
                        <Button variant="outline" className="border-rose-900 text-rose-400 hover:bg-rose-950">
                            <X size={16} className="mr-2" /> Reject Workflow
                        </Button>
                        <Button className="bg-fuchsia-600 hover:bg-fuchsia-700 text-white">
                            <Check size={16} className="mr-2" /> Digitally Sign & Approve
                        </Button>
                    </div>
                </CardContent>
            </Card>

        </div>
    </div>
  );
}

function ApprovalChainNode({ role, status, user, time, active }: any) {
    let icon = <Check size={14} className="text-emerald-500" />;
    let textStyle = "text-slate-300";
    if (status === 'PENDING') {
        icon = <div className="w-2 h-2 rounded-full bg-fuchsia-500 animate-pulse ml-1 mr-0.5"></div>;
        textStyle = "text-fuchsia-400 font-bold";
    }

    return (
        <div className={`flex items-center gap-3 p-2 rounded ${active ? 'bg-slate-950 border border-slate-800' : ''}`}>
            {icon}
            <div className="flex-1 flex justify-between items-center">
                <span className={`text-xs ${textStyle}`}>{role}</span>
                <span className="text-[10px] text-slate-500">{user} • {time}</span>
            </div>
        </div>
    );
}
