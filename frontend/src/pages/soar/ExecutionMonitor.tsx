import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { PlayCircle, CheckCircle, Clock, XCircle, AlertTriangle } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

export default function ExecutionMonitor() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <div className="flex justify-between items-end border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <PlayCircle className="text-cyan-500" />
                Execution Monitor
            </h1>
            <p className="text-slate-400 mt-1">Live view of Playbook Execution: Ransomware Containment</p>
          </div>
          <Badge className="bg-amber-500/20 text-amber-400 border-amber-500/50 text-sm py-1 px-3">
              PAUSED_FOR_APPROVAL
          </Badge>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
                <Card className="bg-slate-900 border-slate-800">
                    <CardHeader>
                        <CardTitle className="text-slate-200 text-sm">Execution Log</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <LogEntry step="Trigger: On Incident Created" status="SUCCESS" time="10:05:12 UTC" />
                        <LogEntry step="Extract IPs & Domains" status="SUCCESS" time="10:05:14 UTC" />
                        <LogEntry step="Enrich IPs (VirusTotal API)" status="SUCCESS" time="10:05:18 UTC" />
                        <LogEntry step="Calculate Risk Score" status="SUCCESS" time="10:05:19 UTC" />
                        <LogEntry step="Approval Gate: Require Manual Auth" status="PAUSED" time="10:05:20 UTC" active />
                        <LogEntry step="Isolate Host (CrowdStrike)" status="PENDING" time="--" pending />
                    </CardContent>
                </Card>
            </div>
            
            <div>
                {/* Approval Action Panel visible because state is PAUSED_FOR_APPROVAL */}
                <Card className="bg-amber-950/20 border-amber-500/30 shadow-[0_0_20px_rgba(245,158,11,0.1)]">
                    <CardHeader>
                        <CardTitle className="text-amber-400 flex items-center gap-2 text-lg">
                            <AlertTriangle size={18} />
                            Action Required
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <p className="text-sm text-slate-300">
                            The workflow has paused at an Approval Gate. Authorize the automation engine to execute containment actions on <strong>HR-05-WORKSTATION</strong>.
                        </p>
                        
                        <div className="bg-slate-950 p-3 rounded border border-slate-800 mt-4">
                            <span className="text-xs font-semibold text-slate-500 uppercase">Context from prior steps:</span>
                            <ul className="text-xs text-slate-300 mt-2 space-y-1">
                                <li>• IP 198.51.100.42 flagged as Malicious (VT Score: 68/89)</li>
                                <li>• Exploit activity matches Ransomware signatures</li>
                            </ul>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 pt-4">
                            <Button variant="outline" className="border-rose-500/50 text-rose-400 bg-rose-950/20 hover:bg-rose-900/50">
                                Reject Execution
                            </Button>
                            <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">
                                Approve & Resume
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    </div>
  );
}

function LogEntry({ step, status, time, active = false, pending = false }: any) {
    let icon = <CheckCircle size={16} className="text-emerald-500" />;
    if (active) icon = <Clock size={16} className="text-amber-500 animate-pulse" />;
    if (pending) icon = <div className="w-4 h-4 rounded-full border-2 border-slate-700"></div>;

    return (
        <div className={`flex items-center justify-between p-3 rounded-lg border ${active ? 'bg-slate-800 border-amber-500/30' : 'bg-slate-950 border-slate-800/50'}`}>
            <div className="flex items-center gap-3">
                {icon}
                <span className={`text-sm ${pending ? 'text-slate-600' : 'text-slate-200'}`}>{step}</span>
            </div>
            <div className="flex items-center gap-4">
                <span className={`text-xs font-mono ${pending ? 'text-slate-600' : 'text-slate-500'}`}>{time}</span>
            </div>
        </div>
    );
}
