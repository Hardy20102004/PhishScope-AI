import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { NotebookPen, ShieldAlert, Crosshair } from 'lucide-react';

export default function CampaignPlanner() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <NotebookPen className="text-rose-400" />
                Campaign Planner & Scope Manager
            </h2>
            <p className="text-slate-400 mt-1">Define objectives, restrict blast radius, and outline Rules of Engagement.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Mission Details */}
            <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-6 space-y-4">
                    <h3 className="text-lg font-bold flex items-center gap-2"><Crosshair size={18} className="text-rose-500"/> Mission Objectives</h3>
                    <p className="text-sm text-slate-400 text-justify">
                        Demonstrate the ability for an unauthenticated external attacker to gain initial access via spearphishing, escalate privileges to Domain Admin, and exfiltrate simulated PII from the production database cluster without triggering SOC alerting.
                    </p>
                    <div className="bg-slate-950 p-3 rounded border border-slate-800 font-mono text-xs text-slate-300">
                        Primary MITRE Tactics: Initial Access, Privilege Escalation, Exfiltration
                    </div>
                </CardContent>
            </Card>

            {/* Scope Constraints */}
            <Card className="bg-slate-900 border-rose-900/50">
                <CardContent className="p-6 space-y-4">
                    <h3 className="text-lg font-bold flex items-center gap-2"><ShieldAlert size={18} className="text-amber-500"/> Rules of Engagement (RoE) & Scope</h3>
                    
                    <div className="space-y-3 font-mono text-xs">
                        <div>
                            <span className="text-emerald-400 block mb-1">IN-SCOPE (Authorized):</span>
                            <ul className="list-disc pl-4 text-slate-300 space-y-1">
                                <li>Corporate Windows Endpoints (10.0.x.x)</li>
                                <li>Active Directory (Read-Only queries)</li>
                            </ul>
                        </div>
                        <div className="border-t border-slate-800 pt-3">
                            <span className="text-rose-500 block mb-1">OUT-OF-SCOPE (Restricted):</span>
                            <ul className="list-disc pl-4 text-slate-300 space-y-1">
                                <li>Production Billing Infrastructure</li>
                                <li>Denial of Service (DoS) of any kind</li>
                                <li>Physical site access</li>
                            </ul>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    </div>
  );
}
