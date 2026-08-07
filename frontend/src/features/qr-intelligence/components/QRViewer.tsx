import React from 'react';

interface QRViewerProps {
    metadata: Record<string, any>;
}

const QRViewer: React.FC<QRViewerProps> = ({ metadata }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full flex flex-col">
            <div className="bg-gray-800 px-4 py-3 border-b border-gray-700">
                <h2 className="text-gray-100 font-semibold">Image Analysis</h2>
            </div>
            
            <div className="p-6 flex-1 flex flex-col">
                <div className="bg-gray-100 rounded-lg h-48 mb-6 flex items-center justify-center border-2 border-dashed border-gray-300 relative">
                    <span className="text-gray-400 text-sm font-medium flex flex-col items-center">
                        <svg className="w-8 h-8 mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                        Mock Render: QR Image
                    </span>
                    
                    {/* Simulated Bounding Box */}
                    <div className="absolute inset-4 border-2 border-green-500 rounded flex items-start justify-end p-1 pointer-events-none">
                         <span className="bg-green-500 text-white text-[10px] font-bold px-1 py-0.5 rounded shadow">QR Detected</span>
                    </div>
                </div>

                <div className="space-y-3 mt-auto">
                    <h3 className="text-sm font-bold text-gray-500 uppercase">Image Metadata</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-gray-50 p-3 rounded border border-gray-200">
                            <span className="block text-xs text-gray-500">Resolution</span>
                            <span className="font-semibold text-gray-700">{metadata.resolution}</span>
                        </div>
                        <div className="bg-gray-50 p-3 rounded border border-gray-200">
                            <span className="block text-xs text-gray-500">File Size</span>
                            <span className="font-semibold text-gray-700">{(metadata.file_size_bytes / 1024).toFixed(1)} KB</span>
                        </div>
                        <div className="bg-gray-50 p-3 rounded border border-gray-200">
                            <span className="block text-xs text-gray-500">Format</span>
                            <span className="font-semibold text-gray-700 uppercase">{metadata.format}</span>
                        </div>
                        <div className="bg-gray-50 p-3 rounded border border-gray-200">
                            <span className="block text-xs text-gray-500">QR Count</span>
                            <span className="font-semibold text-gray-700">{metadata.contains_multiple_qrs ? '> 1' : '1'}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default QRViewer;
