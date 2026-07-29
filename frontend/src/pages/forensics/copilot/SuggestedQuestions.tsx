import React from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';

export default function SuggestedQuestions({ questions }: { questions: string[] }) {
    
    if (!questions || questions.length === 0) return null;

    return (
        <div className="space-y-3">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-wider">
                <Sparkles size={12} className="text-violet-400" />
                Suggested Next Steps
            </div>
            <div className="flex flex-wrap gap-2">
                {questions.map((q, i) => (
                    <button 
                        key={i}
                        className="group flex items-center gap-2 text-xs bg-slate-900 border border-slate-800 hover:border-violet-500/50 hover:bg-violet-950/20 text-slate-300 px-3 py-1.5 rounded transition-all"
                    >
                        {q}
                        <ArrowRight size={12} className="text-slate-600 group-hover:text-violet-400 transition-colors" />
                    </button>
                ))}
            </div>
        </div>
    );
}
