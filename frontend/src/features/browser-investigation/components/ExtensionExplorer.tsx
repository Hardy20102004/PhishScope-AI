import React from 'react';

interface ExtensionExplorerProps {
    extensions: any[];
}

const ExtensionExplorer: React.FC<ExtensionExplorerProps> = ({ extensions }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Installed Extensions</h2>
            
            <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                {extensions.map((ext, idx) => (
                    <div key={idx} className={`p-4 rounded-lg border ${ext.is_suspicious ? 'bg-red-50 border-red-200' : 'bg-gray-50 border-gray-200'}`}>
                        <div className="flex justify-between items-start mb-2">
                            <span className="font-semibold text-gray-900">{ext.name}</span>
                            {ext.is_suspicious && (
                                <span className="bg-red-100 text-red-800 text-[10px] px-2 py-0.5 rounded font-bold uppercase">
                                    SUSPICIOUS
                                </span>
                            )}
                        </div>
                        <div className="text-xs text-gray-500 font-mono mb-2">ID: {ext.extension_id}</div>
                        
                        <div>
                            <span className="text-xs font-semibold text-gray-600 block mb-1">Permissions:</span>
                            <div className="flex flex-wrap gap-1">
                                {ext.permissions.map((perm: string, pIdx: number) => (
                                    <span key={pIdx} className={`text-[10px] px-1.5 py-0.5 rounded border ${
                                        perm === '<all_urls>' ? 'bg-red-100 text-red-700 border-red-200 font-bold' : 'bg-gray-200 text-gray-700 border-gray-300'
                                    }`}>
                                        {perm}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ExtensionExplorer;
