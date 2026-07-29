import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Zap, Code, PlusCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function OptimizationWorkspace() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Zap className="text-amber-400" />
                Detection Optimization Workspace
            </h2>
            <p className="text-slate-400 mt-1">Prioritized engineering backlog to close identified MITRE ATT&CK coverage gaps.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <OptimizationCard 
                technique="T1562.001"
                title="Deploy Detection for 'Disable Windows Event Logging'"
                description="Current coverage is 0%. Attackers frequently use 'auditpol /set' to clear logs before executing ransomware. We need a Splunk correlation search targeting Event ID 4719."
                platform="SPLUNK SIEM"
                coverageImpact="+4.2%"
            />
            
            <OptimizationCard 
                technique="T1048.003"
                title="Create YARA Rule for DNS Exfiltration Tools"
                description="BAS simulations repeatedly bypassed our NDR. We need to deploy a YARA rule via CrowdStrike to target known DNS exfiltration binaries on disk."
                platform="CROWDSTRIKE EDR"
                coverageImpact="+2.8%"
            />
        </div>
    </div>
  );
}

function OptimizationCard({ technique, title, description, platform, coverageImpact }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800 hover:border-cyan-900/50 transition-colors group">
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <span className="text-[10px] font-bold text-slate-500 uppercase flex items-center gap-1 bg-slate-950 px-2 py-1 rounded border border-slate-800">
                        <Code size={12} /> {technique} GAP
                    </span>
                    <span className="text-[10px] font-bold px-2 py-1 rounded border bg-cyan-500/10 text-cyan-400 border-cyan-500/20">
                        TARGET: {platform}
                    </span>
                </div>
                
                <h3 className="text-lg font-bold text-slate-200 mb-2 group-hover:text-cyan-400 transition-colors">{title}</h3>
                <p className="text-sm text-slate-400 mb-6">{description}</p>
                
                <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                    <div className="flex flex-col">
                        <span className="text-[10px] text-slate-500 font-bold uppercase">Estimated Coverage Lift</span>
                        <span className="text-emerald-400 font-black flex items-center gap-1 text-lg">
                            {coverageImpact}
                        </span>
                    </div>
                    
                    <Button variant="outline" className="text-xs h-8 bg-slate-800 border-slate-700 text-slate-300 hover:text-white gap-2">
                        <PlusCircle size={14} /> Assign to Engineer
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}
