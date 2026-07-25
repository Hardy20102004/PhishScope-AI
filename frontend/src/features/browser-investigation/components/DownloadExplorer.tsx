import React from 'react';

interface DownloadExplorerProps {
    downloads: any[];
}

const DownloadExplorer: React.FC<DownloadExplorerProps> = ({ downloads }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Download Forensics</h2>
            
            <div className="space-y-4 max-h-[350px] overflow-y-auto pr-2">
                {downloads.map((dl, idx) => (
                    <div key={idx} className={`p-4 rounded-lg border ${dl.is_malicious ? 'bg-red-50 border-red-200' : 'bg-gray-50 border-gray-200'}`}>
                        <div className="flex justify-between items-start mb-2">
                            <span className="font-semibold text-gray-900">{dl.filename}</span>
                            {dl.is_malicious && (
                                <span className="bg-red-600 text-white text-[10px] px-2 py-0.5 rounded font-bold uppercase">
                                    MALICIOUS
                                </span>
                            )}
                        </div>
                        <div className="text-xs text-blue-600 break-all mb-2">{dl.source_url}</div>
                        <div className="flex justify-between text-xs text-gray-500">
                            <span>{new Date(dl.download_time).toLocaleString()}</span>
                            <span>{(dl.file_size / 1024 / 1024).toFixed(2)} MB</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default DownloadExplorer;
