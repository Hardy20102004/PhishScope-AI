import React from 'react';

interface CommunicationExplorerProps {
    communications: any[];
    iocs: any[];
}

const CommunicationExplorer: React.FC<CommunicationExplorerProps> = ({ communications, iocs }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800 flex items-center justify-between">
                <span>Communications Log</span>
                {iocs.length > 0 && (
                    <span className="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded-full font-bold">
                        {iocs.length} Extracted IOCs
                    </span>
                )}
            </h2>
            
            <div className="space-y-4">
                {communications.map((comm, idx) => (
                    <div key={idx} className="bg-gray-50 border border-gray-200 p-4 rounded-lg">
                        <div className="flex justify-between items-start mb-2">
                            <div>
                                <span className="font-semibold text-gray-900">{comm.contact_number}</span>
                                <span className="text-xs text-gray-500 ml-2">{new Date(comm.timestamp).toLocaleString()}</span>
                            </div>
                            <span className="text-[10px] bg-gray-200 text-gray-700 px-2 py-0.5 rounded font-bold uppercase">
                                {comm.comm_type} - {comm.direction}
                            </span>
                        </div>
                        {comm.body && (
                            <div className="bg-white p-3 border border-gray-100 rounded text-sm text-gray-700 mt-2">
                                {comm.body}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CommunicationExplorer;
