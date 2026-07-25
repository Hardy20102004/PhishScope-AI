import React from 'react';

interface HTTPExplorerProps {
    http: any[];
}

const HTTPExplorer: React.FC<HTTPExplorerProps> = ({ http }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">HTTP Metadata</h2>
            
            <div className="overflow-x-auto max-h-[350px]">
                <table className="w-full text-sm text-left text-gray-500">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 sticky top-0">
                        <tr>
                            <th className="px-4 py-3">Req</th>
                            <th className="px-4 py-3">Host & URI</th>
                            <th className="px-4 py-3">User Agent</th>
                        </tr>
                    </thead>
                    <tbody>
                        {http.map((record, idx) => (
                            <tr key={idx} className="bg-white border-b hover:bg-gray-50">
                                <td className="px-4 py-3 whitespace-nowrap">
                                    <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${record.method === 'POST' ? 'bg-orange-100 text-orange-800' : 'bg-green-100 text-green-800'}`}>
                                        {record.method}
                                    </span>
                                    <div className="mt-1 text-xs font-mono">{record.status_code}</div>
                                </td>
                                <td className="px-4 py-3">
                                    <div className="font-semibold text-gray-900 truncate max-w-[150px]">{record.host}</div>
                                    <div className="text-xs text-blue-600 truncate max-w-[150px]">{record.uri}</div>
                                </td>
                                <td className="px-4 py-3 text-xs text-gray-400 break-all max-w-[150px]">
                                    {record.user_agent}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default HTTPExplorer;
