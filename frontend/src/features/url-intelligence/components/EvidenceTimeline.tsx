import React from 'react';

interface EvidenceTimelineProps {
    chain: any[];
}

const EvidenceTimeline: React.FC<EvidenceTimelineProps> = ({ chain }) => {
    if (!chain || chain.length === 0) {
        return <p className="text-gray-500 italic">No redirects detected.</p>;
    }

    return (
        <div className="relative pl-6 border-l-2 border-gray-200 space-y-6">
            {chain.map((step, idx) => (
                <div key={idx} className="relative">
                    <div className="absolute -left-[31px] bg-white p-1 rounded-full border-2 border-blue-500 mt-1">
                        <div className={`w-3 h-3 rounded-full ${step.redirect_type === 'FINAL' ? 'bg-green-500' : 'bg-blue-500'}`} />
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-100">
                        <div className="flex justify-between items-start mb-2">
                            <span className="text-sm font-semibold text-gray-500 uppercase">Step {step.step_index} • {step.redirect_type}</span>
                            {step.status_code && (
                                <span className={`text-xs font-bold px-2 py-1 rounded ${
                                    step.status_code >= 400 ? 'bg-red-100 text-red-700' : 
                                    step.status_code >= 300 ? 'bg-yellow-100 text-yellow-700' : 
                                    'bg-green-100 text-green-700'
                                }`}>
                                    {step.status_code}
                                </span>
                            )}
                        </div>
                        
                        <div className="space-y-2 text-sm">
                            {step.redirect_type !== 'FINAL' && (
                                <div className="break-all text-gray-600 line-clamp-2">
                                    <span className="font-semibold text-gray-700">From: </span>
                                    {step.from_url}
                                </div>
                            )}
                            <div className={`break-all ${step.redirect_type === 'FINAL' ? 'text-green-700 font-medium' : 'text-blue-600'} line-clamp-2`}>
                                <span className="font-semibold text-gray-700">
                                    {step.redirect_type === 'FINAL' ? 'Landing Page: ' : 'To: '}
                                </span>
                                {step.to_url}
                            </div>
                        </div>
                        
                        {step.response_time_ms && (
                            <div className="mt-3 text-xs text-gray-400">
                                Resolution Time: {Math.round(step.response_time_ms)}ms
                            </div>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default EvidenceTimeline;
