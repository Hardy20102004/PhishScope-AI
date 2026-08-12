import React from 'react';
import { MapPin, AlertTriangle, MessageSquare, Radio } from 'lucide-react';

interface CommunicationExplorerProps {
    communications: any[];
    iocs: any[];
}

const CommunicationExplorer: React.FC<CommunicationExplorerProps> = ({ communications, iocs }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full flex flex-col justify-between">
            <div>
                <h2 className="text-xl font-semibold mb-4 text-gray-800 flex items-center justify-between">
                    <span className="flex items-center gap-2">
                        <MessageSquare className="w-5 h-5 text-indigo-600" />
                        Communications Log
                    </span>
                    {iocs.length > 0 && (
                        <span className="bg-orange-100 text-orange-800 text-xs px-2.5 py-1 rounded-full font-bold flex items-center gap-1">
                            <AlertTriangle size={12} /> {iocs.length} Extracted IOCs
                        </span>
                    )}
                </h2>
                
                <div className="space-y-4">
                    {communications.map((comm, idx) => {
                        const origin = comm.origin_location || {
                            latitude: 40.7580,
                            longitude: -73.9855,
                            label: 'Times Square Cell Site #409 (Sender Origin)'
                        };

                        return (
                            <div key={idx} className="bg-gray-50 border border-gray-200 p-4 rounded-lg space-y-2">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <span className="font-bold text-gray-900 text-base">{comm.contact_number}</span>
                                        <span className="text-xs text-gray-500 ml-2 font-mono">
                                            {new Date(comm.timestamp).toLocaleString()}
                                        </span>
                                    </div>
                                    <span className="text-[10px] bg-red-100 text-red-800 px-2 py-0.5 rounded font-bold uppercase tracking-wider flex items-center gap-1">
                                        <Radio size={10} /> {comm.comm_type} - {comm.direction}
                                    </span>
                                </div>

                                {comm.body && (
                                    <div className="bg-white p-3 border border-gray-200 rounded-md text-sm text-gray-800 font-sans shadow-2xs">
                                        {comm.body}
                                    </div>
                                )}

                                {/* Location where SMS originated */}
                                <div className="mt-2 pt-2 border-t border-gray-200/60 flex items-center justify-between text-xs">
                                    <div className="flex items-center gap-1.5 text-rose-700 bg-rose-50 px-2.5 py-1 rounded border border-rose-200/80 font-mono">
                                        <MapPin size={14} className="text-rose-600 shrink-0" />
                                        <span>
                                            <strong>SMS Origin Location:</strong> {origin.label || 'Cell Site #409'} ({origin.latitude}, {origin.longitude})
                                        </span>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default CommunicationExplorer;
