import React from 'react';

interface TimelineViewerProps {
    timeline: any[];
}

const TimelineViewer: React.FC<TimelineViewerProps> = ({ timeline }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full flex flex-col">
            <div className="bg-blue-50 px-4 py-3 border-b border-blue-100 flex justify-between items-center">
                <h2 className="text-blue-900 font-semibold flex items-center gap-2">
                    Unified Investigation Timeline
                </h2>
                <span className="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded">
                    Chronological
                </span>
            </div>
            
            <div className="p-6 flex-1 overflow-y-auto max-h-[500px]">
                {timeline.length === 0 ? (
                    <p className="text-sm text-gray-500 italic">No timeline events generated.</p>
                ) : (
                    <div className="relative border-l-2 border-blue-200 ml-3 space-y-6">
                        {timeline.map((event, idx) => (
                            <div key={idx} className="relative pl-6">
                                {/* Dot */}
                                <div className="absolute w-3 h-3 bg-blue-500 rounded-full -left-[7px] top-1.5 border-2 border-white shadow"></div>
                                
                                <div className="bg-gray-50 border border-gray-200 p-3 rounded-lg">
                                    <div className="flex justify-between items-start mb-1">
                                        <span className="text-xs font-bold text-gray-500">{new Date(event.timestamp).toLocaleString()}</span>
                                        <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                                            event.event_type === 'LocationUpdate' ? 'bg-purple-100 text-purple-800' :
                                            'bg-green-100 text-green-800'
                                        }`}>
                                            {event.event_type}
                                        </span>
                                    </div>
                                    <p className="text-sm text-gray-800">{event.description}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default TimelineViewer;
