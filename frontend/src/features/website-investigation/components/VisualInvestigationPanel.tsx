import React from 'react';

interface VisualInvestigationPanelProps {
    visual: Record<string, any>;
}

const VisualInvestigationPanel: React.FC<VisualInvestigationPanelProps> = ({ visual }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-semibold mb-4">Visual Layout Analysis</h2>
            
            <div className="flex flex-col md:flex-row gap-6">
                {/* Mock Screenshot */}
                <div className="md:w-1/2">
                    <div className="aspect-video bg-gray-200 rounded-lg overflow-hidden relative border border-gray-300 flex items-center justify-center shadow-inner">
                        <span className="text-gray-400 font-mono text-sm">[Rendered Webpage Capture]</span>
                        {visual.impersonates_brand && (
                            <div className="absolute inset-0 border-4 border-red-500 opacity-50"></div>
                        )}
                    </div>
                </div>
                
                {/* AI Visual Findings */}
                <div className="md:w-1/2 space-y-4">
                    <div className={`p-4 rounded-lg border ${visual.impersonates_brand ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
                        <h3 className="font-semibold text-gray-800 mb-2">Brand Impersonation Check</h3>
                        {visual.impersonates_brand ? (
                            <div>
                                <p className="text-red-700 text-sm font-medium">WARNING: High similarity to known brand detected.</p>
                                <ul className="mt-2 text-sm text-gray-700 space-y-1">
                                    <li><span className="font-semibold">Target Brand:</span> {visual.brand_name}</li>
                                    <li><span className="font-semibold">Similarity:</span> {(visual.similarity_score * 100).toFixed(1)}%</li>
                                    {visual.is_fake_login && <li><span className="font-semibold">Context:</span> Suspicious Login Portal</li>}
                                    {visual.is_fake_banking && <li><span className="font-semibold">Context:</span> Suspicious Banking Portal</li>}
                                </ul>
                            </div>
                        ) : (
                            <p className="text-green-700 text-sm font-medium">No brand impersonation detected in visual layout.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default VisualInvestigationPanel;
