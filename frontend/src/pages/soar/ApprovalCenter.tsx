import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CheckSquare, ShieldAlert, ArrowRight } from 'lucide-react';

export default function ApprovalCenter() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <div className="flex justify-between items-end border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3 text-slate-200">
                <CheckSquare className="text-amber-500" />
                SOAR Approval Center
            </h1>
            <p className="text-slate-400 mt-1">Review and authorize pending automation executions.</p>
          </div>
        </div>

        <div className="space-y-4">
            <ApprovalCard 
                incident="INC-2026-084" 
                workflow="Ransomware Containment (Standard)"
                action="Isolate Host (CrowdStrike): HR-05-WORKSTATION"
                time="2 mins ago"
            />
            <ApprovalCard 
                incident="INC-2026-088" 
                workflow="Compromised Credential Revoke"
                action="Force Password Reset (Azure AD): j.smith@company.com"
                time="15 mins ago"
            />
            <ApprovalCard 
                incident="INC-2026-092" 
                workflow="Block Malicious Infrastructure"
                action="Add IP 198.51.100.42 to Firewall Deny List"
                time="1 hour ago"
            />
        </div>
    </div>
  );
}

function ApprovalCard({ incident, workflow, action, time }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800 hover:border-slate-600 transition-colors">
            <CardContent className="p-6 flex items-center justify-between">
                <div className="flex items-start gap-4">
                    <div className="p-3 bg-amber-500/10 text-amber-500 rounded-lg">
                        <ShieldAlert size={24} />
                    </div>
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                            <span className="text-xs font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-400">{incident}</span>
                            <span className="text-xs text-slate-500">via Playbook: {workflow}</span>
                        </div>
                        <h3 className="text-lg font-semibold text-slate-200 mt-2">{action}</h3>
                        <p className="text-sm text-slate-500 mt-1">Requested {time}</p>
                    </div>
                </div>
                
                <div className="flex gap-2">
                    <Button variant="outline" className="border-rose-500/50 text-rose-400 bg-rose-950/20 hover:bg-rose-900/50">
                        Reject
                    </Button>
                    <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">
                        Review & Approve <ArrowRight size={14} className="ml-2" />
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}
