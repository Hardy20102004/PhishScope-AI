import React from 'react';

interface RoutingTimelineProps {
    routing: any[];
}

const RoutingTimeline: React.FC<RoutingTimelineProps> = ({ routing }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-6">Routing Hops (Received Chain)</h2>
            
            {routing.length === 0 ? (
                <p className="text-gray-500 italic text-sm">No routing hops detected.</p>
            ) : (
                <div className="relative border-l-2 border-blue-200 ml-3 space-y-6">
                    {routing.map((hop, idx) => (
                        <div key={idx} className="relative pl-6">
                            {/* Dot */}
                            <span className="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-blue-500 border-2 border-white"></span>
                            
                            <div className="bg-gray-50 p-3 rounded border border-gray-200 shadow-sm">
                                <div className="flex justify-between items-start mb-1">
                                    <span className="text-sm font-bold text-gray-700">Hop {hop.hop_index}</span>
                                    {idx === 0 && <span className="text-xs font-bold text-red-500 bg-red-50 px-2 py-0.5 rounded">ORIGIN</span>}
                                    {idx === routing.length - 1 && <span className="text-xs font-bold text-green-500 bg-green-50 px-2 py-0.5 rounded">DESTINATION</span>}
                                </div>
                                <div className="text-xs text-gray-600 space-y-1">
                                    <p><span className="font-semibold">IP:</span> {hop.sending_ip}</p>
                                    <p className="font-mono text-[10px] text-gray-400 mt-2 truncate" title={hop.raw}>{hop.raw}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default RoutingTimeline;
