import React from 'react';
import { Eye, BrainCircuit, Lightbulb, HelpCircle } from 'lucide-react';

export default function ExplanationBadge({ type }: { type: 'OBSERVATION' | 'ASSESSMENT' | 'RECOMMENDATION' | 'UNKNOWN' }) {
    
    const config = {
        OBSERVATION: {
            icon: <Eye size={12} />,
            label: "EVIDENCE",
            classes: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
            tooltip: "Fact directly extracted from parsed evidence artifacts."
        },
        ASSESSMENT: {
            icon: <BrainCircuit size={12} />,
            label: "AI INFERENCE",
            classes: "bg-sky-500/10 text-sky-400 border-sky-500/30",
            tooltip: "Analytical conclusion inferred by the AI."
        },
        RECOMMENDATION: {
            icon: <Lightbulb size={12} />,
            label: "NEXT STEP",
            classes: "bg-violet-500/10 text-violet-400 border-violet-500/30",
            tooltip: "Recommended investigative action."
        },
        UNKNOWN: {
            icon: <HelpCircle size={12} />,
            label: "GAP",
            classes: "bg-rose-500/10 text-rose-400 border-rose-500/30",
            tooltip: "Missing information required to complete analysis."
        }
    }[type];

    if (!config) return null;

    return (
        <div className={`flex items-center gap-1.5 px-2 py-1 rounded text-[10px] font-bold tracking-wider border shrink-0 mt-0.5 self-start cursor-help ${config.classes}`} title={config.tooltip}>
            {config.icon}
            {config.label}
        </div>
    );
}
