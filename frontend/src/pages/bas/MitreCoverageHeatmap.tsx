import React from 'react';
import { LayoutGrid, AlertTriangle } from 'lucide-react';

export default function MitreCoverageHeatmap() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="border-b border-slate-800 pb-4 mb-6">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                <LayoutGrid className="text-fuchsia-400" />
                MITRE ATT&CK® Detection Coverage
            </h2>
            <p className="text-slate-400 mt-1">Aggregated validation results mapped to the MITRE enterprise matrix.</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-1 font-mono text-xs">
            <HeatmapBlock tactic="Initial Access" score={85} />
            <HeatmapBlock tactic="Execution" score={92} />
            <HeatmapBlock tactic="Persistence" score={40} alert={true} />
            <HeatmapBlock tactic="Privilege Escalation" score={78} />
            <HeatmapBlock tactic="Defense Evasion" score={30} alert={true} />
            <HeatmapBlock tactic="Credential Access" score={95} />
            <HeatmapBlock tactic="Discovery" score={88} />
            <HeatmapBlock tactic="Lateral Movement" score={75} />
            <HeatmapBlock tactic="Collection" score={65} />
            <HeatmapBlock tactic="Command and Control" score={72} />
            <HeatmapBlock tactic="Exfiltration" score={50} alert={true} />
            <HeatmapBlock tactic="Impact" score={90} />
        </div>
    </div>
  );
}

function HeatmapBlock({ tactic, score, alert }: any) {
    let bgClass = "bg-slate-900";
    let textClass = "text-slate-500";
    
    if (score >= 80) {
        bgClass = "bg-emerald-950/40 border-emerald-900";
        textClass = "text-emerald-400";
    } else if (score >= 60) {
        bgClass = "bg-amber-950/30 border-amber-900/50";
        textClass = "text-amber-400";
    } else if (score > 0) {
        bgClass = "bg-rose-950/40 border-rose-900/50";
        textClass = "text-rose-400";
    }

    return (
        <div className={`p-4 border ${bgClass} rounded flex flex-col h-32 relative overflow-hidden group hover:border-slate-500 transition-colors cursor-pointer`}>
            {alert && <AlertTriangle size={14} className="absolute top-2 right-2 text-rose-500 animate-pulse" />}
            <span className="text-[10px] text-slate-400 font-bold uppercase mb-auto leading-tight">{tactic}</span>
            <div className={`text-2xl font-black mt-2 ${textClass}`}>{score}%</div>
            
            {/* Hover details */}
            <div className="absolute inset-0 bg-slate-900/95 p-2 flex flex-col justify-center items-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span className="text-[10px] text-slate-300 text-center">View TTP Details</span>
            </div>
        </div>
    );
}
