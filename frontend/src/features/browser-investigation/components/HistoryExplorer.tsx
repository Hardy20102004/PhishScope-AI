import React from 'react';

interface HistoryExplorerProps {
    history: any[];
}

const HistoryExplorer: React.FC<HistoryExplorerProps> = ({ history }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Browsing History</h2>
            
            <div className="overflow-x-auto max-h-[350px]">
                <table className="w-full text-sm text-left text-gray-500">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 sticky top-0">
                        <tr>
                            <th className="px-4 py-3">Time</th>
                            <th className="px-4 py-3">Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.map((record, idx) => (
                            <tr key={idx} className="bg-white border-b hover:bg-gray-50">
                                <td className="px-4 py-3 whitespace-nowrap text-xs">
                                    {new Date(record.visit_time).toLocaleString()}
                                </td>
                                <td className="px-4 py-3">
                                    <div className="font-medium text-gray-900">{record.title || 'No Title'}</div>
                                    <div className="text-xs text-blue-600 truncate max-w-xs">{record.url}</div>
                                    {record.is_search && (
                                        <span className="mt-1 inline-block bg-yellow-100 text-yellow-800 text-[10px] px-2 py-0.5 rounded font-bold uppercase">
                                            Search: {record.search_keyword}
                                        </span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default HistoryExplorer;
