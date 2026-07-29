import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ShieldAlert, Crosshair, Network } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function RiskPosture() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans">
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h1 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <ShieldAlert className="text-rose-500" />
                Security Risk Posture
            </h1>
            <p className="text-slate-400 mt-1">MITRE ATT&CK coverage gaps and active threat exposure analysis.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Card className="bg-slate-900 border-slate-800 lg:col-span-2">
                <CardHeader>
                    <CardTitle className="text-slate-200 flex items-center gap-2 text-sm uppercase tracking-wider">
                        <Crosshair size={16} className="text-slate-500" /> MITRE ATT&CK Tactic Coverage
                    </CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <CoverageCard tactic="Initial Access" score="High" color="emerald" />
                    <CoverageCard tactic="Execution" score="High" color="emerald" />
                    <CoverageCard tactic="Persistence" score="Medium" color="amber" />
                    <CoverageCard tactic="Privilege Escalation" score="High" color="emerald" />
                    <CoverageCard tactic="Defense Evasion" score="Medium" color="amber" />
                    <CoverageCard tactic="Credential Access" score="High" color="emerald" />
                    <CoverageCard tactic="Lateral Movement" score="Low" color="rose" />
                    <CoverageCard tactic="Exfiltration" score="High" color="emerald" />
                </CardContent>
            </Card>
            
            <Card className="bg-slate-900 border-slate-800">
                <CardHeader>
                    <CardTitle className="text-slate-200 flex items-center gap-2 text-sm uppercase tracking-wider">
                        <Network size={16} className="text-slate-500" /> Active Threat Exposure
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="bg-rose-950/20 border border-rose-500/30 p-4 rounded-lg">
                        <h4 className="text-rose-400 font-bold text-sm mb-1">Unmitigated CVE-2026-9912</h4>
                        <p className="text-xs text-slate-400 mb-3">Critical vulnerability present on 14 public-facing Edge servers.</p>
                        <Badge variant="outline" className="bg-rose-900/50 text-rose-300 border-rose-500/50 text-[10px]">RISK: CRITICAL</Badge>
                    </div>
                    
                    <div className="bg-amber-950/20 border border-amber-500/30 p-4 rounded-lg">
                        <h4 className="text-amber-400 font-bold text-sm mb-1">APT29 Reconnaissance</h4>
                        <p className="text-xs text-slate-400 mb-3">Elevated scanning activity originating from known TOR exit nodes against Cloud VPN gateways.</p>
                        <Badge variant="outline" className="bg-amber-900/50 text-amber-300 border-amber-500/50 text-[10px]">RISK: ELEVATED</Badge>
                    </div>
                </CardContent>
            </Card>
        </div>
    </div>
  );
}

function CoverageCard({ tactic, score, color }: any) {
    return (
        <div className={`p-4 rounded-lg border bg-slate-950/50 border-${color}-500/20`}>
            <div className="flex justify-between items-start mb-2">
                <span className="text-xs font-semibold text-slate-300 leading-tight">{tactic}</span>
            </div>
            <span className={`text-xl font-bold text-${color}-400`}>{score}</span>
        </div>
    );
}
