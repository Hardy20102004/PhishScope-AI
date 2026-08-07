import React from 'react';

interface AttachmentExplorerProps {
    attachments: any[];
}

const AttachmentExplorer: React.FC<AttachmentExplorerProps> = ({ attachments }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full flex flex-col">
            <div className="bg-orange-50 px-4 py-3 border-b border-orange-100 flex justify-between items-center">
                <h2 className="text-orange-900 font-semibold">Attachments ({attachments.length})</h2>
            </div>
            
            <div className="p-0 flex-1">
                {attachments.length === 0 ? (
                    <p className="text-gray-500 italic text-sm p-6">No attachments found.</p>
                ) : (
                    <ul className="divide-y divide-gray-100">
                        {attachments.map((att, idx) => (
                            <li key={idx} className="p-4 hover:bg-gray-50">
                                <div className="flex justify-between items-start mb-2">
                                    <span className="font-semibold text-gray-800 break-all pr-2">{att.filename}</span>
                                    {att.is_suspicious && <span className="bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded flex-shrink-0">SUSPICIOUS</span>}
                                </div>
                                <div className="text-xs text-gray-500 space-y-1">
                                    <p><span className="font-semibold">Type:</span> {att.content_type}</p>
                                    <p><span className="font-semibold">Size:</span> {(att.size_bytes / 1024).toFixed(2)} KB</p>
                                    <p className="font-mono text-[10px] break-all bg-gray-100 p-1 rounded mt-1">SHA256: {att.sha256_hash}</p>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default AttachmentExplorer;
