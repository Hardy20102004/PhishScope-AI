import React from 'react';

interface CloudAIFindingsProps {
    summary: {
        risk_narrative: string;
        threat_summary: string;
        recommended_next_steps: string;
        evidence_correlation: string;
    };
}

const CloudAIFindings: React.FC<CloudAIFindingsProps> = ({ summary }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-indigo-100 h-full">
            <h2 className="text-xl font-semibold flex items-center gap-2 mb-4">
                <span className="text-indigo-600">✧</span> AI Forensic Narrative
            </h2>
            
            <div className="space-y-4">
                <div>
                    <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-1">Executive Summary</h3>
                    <p className="text-slate-800 leading-relaxed text-lg">{summary.risk_narrative}</p>
                </div>
                
                <div>
                    <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Detected Threat Indicators</h3>
                    <div className="flex flex-wrap gap-2">
                        {summary.threat_summary.split(', ').map((threat, idx) => (
                            <span key={idx} className="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-sm font-medium border border-indigo-200">
                                {threat}
                            </span>
                        ))}
                    </div>
                </div>

                <div className="bg-amber-50 p-4 rounded-lg border border-amber-100 mt-4">
                    <h3 className="text-sm font-semibold text-amber-800 uppercase tracking-wider mb-1">Recommended Action</h3>
                    <p className="text-amber-900 font-medium">{summary.recommended_next_steps}</p>
                </div>
            </div>
        </div>
    );
};

export default CloudAIFindings;
