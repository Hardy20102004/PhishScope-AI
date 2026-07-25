import React from 'react';

interface TimelineViewerProps {
    timeline: any[];
}

const TimelineViewer: React.FC<TimelineViewerProps> = ({ timeline }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden h-full flex flex-col">
            <div className="bg-indigo-50 px-4 py-3 border-b border-indigo-100 flex justify-between items-center">
                <h2 className="text-indigo-900 font-semibold flex items-center gap-2">
                    Unified Cloud Timeline
                </h2>
                <span className="bg-indigo-600 text-white text-xs font-bold px-3 py-1 rounded">
                    Chronological
                </span>
            </div>
            
            <div className="p-6 flex-1 overflow-y-auto max-h-[400px]">
                {timeline.length === 0 ? (
                    <p className="text-sm text-slate-500 italic">No timeline events generated.</p>
                ) : (
                    <div className="relative border-l-2 border-indigo-200 ml-3 space-y-6">
                        {timeline.map((event, idx) => (
                            <div key={idx} className="relative pl-6">
                                {/* Dot */}
                                <div className="absolute w-3 h-3 bg-indigo-500 rounded-full -left-[7px] top-1.5 border-2 border-white shadow"></div>
                                
                                <div className="bg-slate-50 border border-slate-200 p-3 rounded-lg">
                                    <div className="flex justify-between items-start mb-1">
                                        <span className="text-xs font-bold text-slate-500">{new Date(event.timestamp).toLocaleString()}</span>
                                        <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                                            event.event_type === 'Audit' ? 'bg-amber-100 text-amber-800' :
                                            'bg-slate-200 text-slate-800'
                                        }`}>
                                            {event.event_type}
                                        </span>
                                    </div>
                                    <p className="text-sm text-slate-800 break-all">{event.description}</p>
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
