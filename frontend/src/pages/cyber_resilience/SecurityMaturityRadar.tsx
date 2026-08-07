import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Target, Info } from 'lucide-react';

export default function SecurityMaturityRadar() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <Target className="text-cyan-400" />
                Enterprise Security Maturity Assessment
            </h2>
            <p className="text-slate-400 mt-1">Operational data mapped to standard 5-tier maturity capabilities across core domains.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* Mock Radar Chart Area */}
            <Card className="bg-slate-900 border-slate-800 flex items-center justify-center py-12 relative">
                <div className="absolute top-4 right-4 text-slate-500 hover:text-slate-300 cursor-pointer">
                    <Info size={20} />
                </div>
                
                {/* SVG implementation of a radar chart for visual flair */}
                <svg width="400" height="400" viewBox="-200 -200 400 400">
                    {/* Concentric grid lines (Tiers 1 to 5) */}
                    {[1, 2, 3, 4, 5].map(tier => (
                        <polygon 
                            key={tier}
                            points="0,-150 142,-46 88,121 -88,121 -142,-46"
                            fill="none" 
                            stroke="#334155" 
                            strokeWidth="1"
                            transform={`scale(${tier * 0.2})`}
                        />
                    ))}
                    
                    {/* Axis lines */}
                    <line x1="0" y1="0" x2="0" y2="-150" stroke="#475569" strokeWidth="1" strokeDasharray="4 4" />
                    <line x1="0" y1="0" x2="142" y2="-46" stroke="#475569" strokeWidth="1" strokeDasharray="4 4" />
                    <line x1="0" y1="0" x2="88" y2="121" stroke="#475569" strokeWidth="1" strokeDasharray="4 4" />
                    <line x1="0" y1="0" x2="-88" y2="121" stroke="#475569" strokeWidth="1" strokeDasharray="4 4" />
                    <line x1="0" y1="0" x2="-142" y2="-46" stroke="#475569" strokeWidth="1" strokeDasharray="4 4" />

                    {/* Labels */}
                    <text x="0" y="-160" fill="#94a3b8" fontSize="12" textAnchor="middle" fontWeight="bold">SOC Ops</text>
                    <text x="150" y="-50" fill="#94a3b8" fontSize="12" textAnchor="start" fontWeight="bold">AppSec</text>
                    <text x="95" y="135" fill="#94a3b8" fontSize="12" textAnchor="start" fontWeight="bold">Identity</text>
                    <text x="-95" y="135" fill="#94a3b8" fontSize="12" textAnchor="end" fontWeight="bold">DFIR</text>
                    <text x="-150" y="-50" fill="#94a3b8" fontSize="12" textAnchor="end" fontWeight="bold">Detection</text>

                    {/* Data Polygon (Current Maturity) */}
                    {/* Tiers: SOC=4, AppSec=3, Identity=5, DFIR=4, Detection=3 */}
                    <polygon 
                        points="0,-120 85.2,-27.6 88,121 -70.4,96.8 -85.2,-27.6"
                        fill="rgba(16, 185, 129, 0.2)" 
                        stroke="#34d399" 
                        strokeWidth="2"
                    />
                    
                    {/* Data Points */}
                    <circle cx="0" cy="-120" r="4" fill="#10b981" />
                    <circle cx="85.2" cy="-27.6" r="4" fill="#10b981" />
                    <circle cx="88" cy="121" r="4" fill="#10b981" />
                    <circle cx="-70.4" cy="96.8" r="4" fill="#10b981" />
                    <circle cx="-85.2" cy="-27.6" r="4" fill="#10b981" />
                </svg>
            </Card>

            {/* Maturity Details */}
            <div className="space-y-4">
                <MaturityRow domain="Identity Security" tier={5} desc="Optimizing. Automated RBAC, mandatory phishing-resistant MFA, zero-trust enforcement." color="text-fuchsia-400" />
                <MaturityRow domain="SOC Operations" tier={4} desc="Quantitatively Managed. SOAR-driven triage, strict MTTR KPIs, continuous BAS validation." color="text-emerald-400" />
                <MaturityRow domain="DFIR Readiness" tier={4} desc="Quantitatively Managed. Full endpoint telemetry retention, automated evidence collection." color="text-emerald-400" />
                <MaturityRow domain="Detection Engineering" tier={3} desc="Defined. MITRE-aligned ruleset, basic CI/CD pipeline, but relies on manual tuning." color="text-amber-400" />
                <MaturityRow domain="Application Security" tier={3} desc="Defined. Static analysis in CI pipelines, but lacks runtime RASP protection." color="text-amber-400" />
            </div>

        </div>
    </div>
  );
}

function MaturityRow({ domain, tier, desc, color }: any) {
    return (
        <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-4 flex items-center justify-between">
                <div>
                    <h3 className="text-sm font-bold text-slate-200">{domain}</h3>
                    <p className="text-xs text-slate-500 mt-1">{desc}</p>
                </div>
                <div className="flex flex-col items-end min-w-[80px]">
                    <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Tier</span>
                    <span className={`text-2xl font-black ${color}`}>{tier}</span>
                </div>
            </CardContent>
        </Card>
    );
}
