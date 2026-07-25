import React from 'react';

interface PayloadViewerProps {
    decoded: Record<string, any>;
}

const PayloadViewer: React.FC<PayloadViewerProps> = ({ decoded }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full flex flex-col">
            <div className="bg-blue-50 px-4 py-3 border-b border-blue-100 flex justify-between items-center">
                <h2 className="text-blue-900 font-semibold flex items-center gap-2">
                    Decoded Payload
                </h2>
                <span className="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded uppercase">
                    {decoded.payload_type}
                </span>
            </div>
            
            <div className="p-6 flex-1">
                <div className="mb-6">
                    <h3 className="text-sm font-bold text-gray-500 uppercase mb-2">Raw Extracted String</h3>
                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 font-mono text-sm text-gray-800 break-all max-h-[150px] overflow-y-auto">
                        {decoded.raw_payload}
                    </div>
                </div>

                {decoded.extracted_url && (
                    <div>
                        <h3 className="text-sm font-bold text-gray-500 uppercase mb-2">Extracted URL</h3>
                        <div className="bg-red-50 p-3 rounded-lg border border-red-200 flex justify-between items-center">
                            <span className="text-red-700 font-mono text-sm truncate pr-4">{decoded.extracted_url}</span>
                            <span className="text-xs font-bold text-red-600 bg-red-100 px-2 py-1 rounded flex-shrink-0">High Risk Indicator</span>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PayloadViewer;
