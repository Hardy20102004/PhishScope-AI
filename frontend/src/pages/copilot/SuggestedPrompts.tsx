import React from 'react';
import { Terminal, FileText, Search } from 'lucide-react';

export default function SuggestedPrompts() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <PromptCard 
            icon={<Search size={16} className="text-amber-400" />}
            title="Refine Hunt Query"
            description="Generate a KQL query to find similar SMB enumeration."
        />
        <PromptCard 
            icon={<Terminal size={16} className="text-emerald-400" />}
            title="Isolate Host"
            description="Trigger the SOAR playbook to contain HR-05 immediately."
        />
        <PromptCard 
            icon={<FileText size={16} className="text-blue-400" />}
            title="Draft Report"
            description="Summarize these findings into an Executive Briefing."
        />
    </div>
  );
}

function PromptCard({ icon, title, description }: any) {
    return (
        <div className="p-3 bg-slate-900/50 hover:bg-slate-800 rounded-lg border border-slate-800 hover:border-slate-600 transition-all cursor-pointer group">
            <div className="flex items-center gap-2 mb-1">
                {icon}
                <span className="text-sm font-semibold text-slate-200 group-hover:text-white transition-colors">{title}</span>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed">{description}</p>
        </div>
    );
}
