import React from 'react';

interface WebsiteAIFindingsProps {
    summary: {
        risk_narrative: string;
        threat_summary: string;
        recommended_next_steps: string;
        evidence_correlation: string;
    };
}

const WebsiteAIFindings: React.FC<WebsiteAIFindingsProps> = ({ summary }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-purple-100 h-full">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <span className="text-purple-600">✧</span> Website Behavior Analysis (AI Brain)
            </h2>
            
            <div className="space-y-4">
                <div>
                    <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Threat Narrative</h3>
                    <p className="text-gray-800 leading-relaxed text-lg">{summary.risk_narrative}</p>
                </div>
                
                <div>
                    <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Detected Behaviors</h3>
                    <div className="flex flex-wrap gap-2">
                        {summary.threat_summary.split(', ').map((threat, idx) => (
                            <span key={idx} className="bg-purple-50 text-purple-700 px-3 py-1 rounded-full text-sm font-medium border border-purple-200">
                                {threat}
                            </span>
                        ))}
                    </div>
                </div>

                <div className="bg-orange-50 p-4 rounded-lg border border-orange-100 mt-4">
                    <h3 className="text-sm font-semibold text-orange-800 uppercase tracking-wider mb-1">Recommended Action</h3>
                    <p className="text-orange-900 font-medium">{summary.recommended_next_steps}</p>
                </div>
            </div>
        </div>
    );
};

export default WebsiteAIFindings;
