import React from 'react';

interface ConversationViewerProps {
    conversation: Record<string, any>;
}

const ConversationViewer: React.FC<ConversationViewerProps> = ({ conversation }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full flex flex-col">
            <div className="bg-blue-50 px-4 py-3 border-b border-blue-100 flex justify-between items-center">
                <h2 className="text-blue-900 font-semibold">Conversation & Links</h2>
                {conversation.is_bec_suspect && (
                    <span className="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">BEC SUSPECT</span>
                )}
            </div>
            
            <div className="p-6 flex-1">
                <div className="mb-6">
                    <h3 className="text-sm font-bold text-gray-500 uppercase mb-2">Linguistic Analysis</h3>
                    <div className="flex gap-4">
                        <div className="bg-gray-50 p-3 rounded border border-gray-200 flex-1">
                            <span className="block text-xs text-gray-500 mb-1">Urgency Indicators</span>
                            <span className={`text-xl font-bold ${conversation.urgency_indicators_found > 0 ? 'text-red-500' : 'text-green-500'}`}>
                                {conversation.urgency_indicators_found}
                            </span>
                        </div>
                    </div>
                </div>

                <div>
                    <h3 className="text-sm font-bold text-gray-500 uppercase mb-2">Extracted URLs ({conversation.extracted_urls?.length || 0})</h3>
                    {conversation.extracted_urls?.length === 0 ? (
                        <p className="text-sm text-gray-500 italic">No URLs found in body.</p>
                    ) : (
                        <ul className="space-y-2 max-h-[300px] overflow-y-auto pr-2">
                            {conversation.extracted_urls.map((u: any, idx: number) => (
                                <li key={idx} className="bg-gray-50 p-2 rounded border border-gray-200 flex justify-between items-center">
                                    <span className="text-sm text-blue-600 font-mono truncate max-w-[80%]" title={u.url}>{u.url}</span>
                                    <span className="text-xs text-gray-500 bg-gray-200 px-2 py-0.5 rounded">{u.context}</span>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ConversationViewer;
