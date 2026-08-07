import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { BookOpen, Play, ShieldAlert, CheckCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function ScenarioLibrary() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <BookOpen className="text-sky-400" />
                Validation Scenario Library
            </h2>
            <p className="text-slate-400 mt-1">Authorized, safe templates for testing security controls mapped to MITRE ATT&CK.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ScenarioCard 
                name="Spearphishing Attachment Execution" 
                tactic="Initial Access" 
                technique="T1566.001"
                description="Simulates the detonation of a macro-enabled document, attempting to drop a benign payload to disk."
                controls={["Email Gateway", "EDR"]}
                complexity="LOW"
            />
            <ScenarioCard 
                name="Kerberoasting & Lateral Movement" 
                tactic="Credential Access" 
                technique="T1558.003"
                description="Simulates requesting service tickets for vulnerable AD accounts to test identity protection rules."
                controls={["SIEM", "Identity Protection"]}
                complexity="HIGH"
            />
        </div>
    </div>
  );
}

function ScenarioCard({ name, tactic, technique, description, controls, complexity }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
            <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <Badge className="bg-sky-500/10 text-sky-400 border-sky-500/30 font-mono">{technique}</Badge>
                    <span className={`text-[10px] font-bold px-2 py-1 rounded ${complexity === 'HIGH' ? 'bg-rose-500/10 text-rose-400' : 'bg-emerald-500/10 text-emerald-400'}`}>
                        {complexity} COMPLEXITY
                    </span>
                </div>
                
                <h3 className="text-lg font-bold text-slate-200 mb-1">{name}</h3>
                <p className="text-xs text-sky-500 font-bold uppercase tracking-wider mb-3">{tactic}</p>
                <p className="text-sm text-slate-400 mb-6">{description}</p>
                
                <div className="space-y-4 font-mono text-xs">
                    <div>
                        <span className="text-slate-500 block mb-1">Target Controls:</span>
                        <div className="flex gap-2">
                            {controls.map((c: string) => (
                                <span key={c} className="bg-slate-950 border border-slate-800 px-2 py-1 rounded text-slate-300">{c}</span>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="mt-6 pt-4 border-t border-slate-800 flex justify-end">
                    <button className="flex items-center gap-2 text-sm font-bold text-emerald-400 hover:text-emerald-300 transition-colors">
                        <Play size={16} /> Run Validation
                    </button>
                </div>
            </CardContent>
        </Card>
    );
}
