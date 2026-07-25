import React from 'react';

interface CodeExplorerProps {
    html: Record<string, any>;
    js: any[];
}

const CodeExplorer: React.FC<CodeExplorerProps> = ({ html, js }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden h-full">
            <div className="bg-gray-800 px-4 py-3 border-b border-gray-700 flex justify-between items-center">
                <h2 className="text-gray-100 font-semibold">Code Analysis (HTML & JS)</h2>
            </div>
            
            <div className="p-6 space-y-6">
                <div>
                    <h3 className="font-semibold text-gray-700 mb-3 border-b pb-2">DOM & HTML Indicators</h3>
                    <ul className="space-y-2">
                        <li className="flex items-center gap-2">
                            <span className={`w-3 h-3 rounded-full ${html.has_hidden_elements ? 'bg-red-500' : 'bg-green-500'}`}></span>
                            <span>Hidden Elements (display:none)</span>
                        </li>
                        <li className="flex items-center gap-2">
                            <span className={`w-3 h-3 rounded-full ${html.embedded_credentials ? 'bg-red-500' : 'bg-green-500'}`}></span>
                            <span>Embedded Credentials in Source</span>
                        </li>
                        <li className="flex items-center gap-2">
                            <span className={`w-3 h-3 rounded-full ${html.has_iframes ? 'bg-yellow-500' : 'bg-green-500'}`}></span>
                            <span>Contains iframes</span>
                        </li>
                        <li className="flex items-center gap-2">
                            <span className={`w-3 h-3 rounded-full ${html.has_meta_refresh ? 'bg-yellow-500' : 'bg-green-500'}`}></span>
                            <span>Meta Refresh Tags</span>
                        </li>
                    </ul>
                </div>
                
                <div>
                    <h3 className="font-semibold text-gray-700 mb-3 border-b pb-2">JavaScript Execution Context</h3>
                    {js.length === 0 ? (
                        <p className="text-gray-500 italic text-sm">No scripts detected.</p>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="min-w-full text-sm">
                                <thead>
                                    <tr className="bg-gray-50 text-gray-600 text-left">
                                        <th className="py-2 px-3">Source</th>
                                        <th className="py-2 px-3 text-center">Obfuscated</th>
                                        <th className="py-2 px-3 text-center">Suspicious APIs</th>
                                        <th className="py-2 px-3 text-center">Tracking</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-100">
                                    {js.map((script, idx) => (
                                        <tr key={idx} className="hover:bg-gray-50">
                                            <td className="py-2 px-3 font-mono text-xs truncate max-w-[200px]" title={script.script_source}>
                                                {script.script_source === 'inline' ? '<inline script>' : script.script_source}
                                            </td>
                                            <td className="py-2 px-3 text-center">
                                                {script.is_obfuscated ? <span className="text-red-500 font-bold">YES</span> : <span className="text-gray-300">-</span>}
                                            </td>
                                            <td className="py-2 px-3 text-center">
                                                {script.uses_suspicious_apis ? <span className="text-yellow-600 font-bold">YES</span> : <span className="text-gray-300">-</span>}
                                            </td>
                                            <td className="py-2 px-3 text-center">
                                                {script.is_tracking_library ? <span className="text-blue-500 font-bold">YES</span> : <span className="text-gray-300">-</span>}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CodeExplorer;
