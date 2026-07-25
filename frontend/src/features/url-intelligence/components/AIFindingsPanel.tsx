import React from 'react';

interface AIFindingsPanelProps {
    summary: {
        risk_narrative: string;
        threat_summary: string;
        recommended_next_steps: string;
        evidence_correlation: string;
    };
}

const AIFindingsPanel: React.FC<AIFindingsPanelProps> = ({ summary }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <span className="text-blue-600">✧</span> AI Security Brain Findings
            </h2>
            
            <div className="space-y-4">
                <div>
                    <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Risk Narrative</h3>
                    <p className="text-gray-800 leading-relaxed">{summary.risk_narrative}</p>
                </div>
                
                <div>
                    <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Threat Summary</h3>
                    <div className="flex flex-wrap gap-2">
                        {summary.threat_summary.split(', ').map((threat, idx) => (
                            <span key={idx} className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm font-medium">
                                {threat}
                            </span>
                        ))}
                    </div>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                    <h3 className="text-sm font-semibold text-blue-800 uppercase tracking-wider mb-1">Recommended Action</h3>
                    <p className="text-blue-900 font-medium">{summary.recommended_next_steps}</p>
                </div>
            </div>
        </div>
    );
};

export default AIFindingsPanel;
