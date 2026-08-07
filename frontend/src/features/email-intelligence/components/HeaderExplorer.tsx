import React from 'react';

interface HeaderExplorerProps {
    headers: Record<string, any>;
}

const HeaderExplorer: React.FC<HeaderExplorerProps> = ({ headers }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="bg-gray-800 px-4 py-3 border-b border-gray-700">
                <h2 className="text-gray-100 font-semibold">Message Headers</h2>
            </div>
            <div className="p-0">
                <table className="min-w-full text-sm">
                    <tbody className="divide-y divide-gray-100">
                        <tr className="hover:bg-gray-50">
                            <th className="py-3 px-4 text-left font-semibold text-gray-600 bg-gray-50 w-1/4">Subject</th>
                            <td className="py-3 px-4 text-gray-800 font-medium">{headers.subject}</td>
                        </tr>
                        <tr className="hover:bg-gray-50">
                            <th className="py-3 px-4 text-left font-semibold text-gray-600 bg-gray-50">From</th>
                            <td className="py-3 px-4 text-gray-800">{headers.from_address}</td>
                        </tr>
                        <tr className="hover:bg-gray-50">
                            <th className="py-3 px-4 text-left font-semibold text-gray-600 bg-gray-50">To</th>
                            <td className="py-3 px-4 text-gray-800">{headers.to_addresses?.join(', ')}</td>
                        </tr>
                        <tr className="hover:bg-gray-50">
                            <th className="py-3 px-4 text-left font-semibold text-gray-600 bg-gray-50">Date</th>
                            <td className="py-3 px-4 text-gray-800">{headers.date_sent}</td>
                        </tr>
                        <tr className="hover:bg-gray-50">
                            <th className="py-3 px-4 text-left font-semibold text-gray-600 bg-gray-50">Message-ID</th>
                            <td className="py-3 px-4 text-gray-500 font-mono text-xs">{headers.message_id}</td>
                        </tr>
                        <tr className="hover:bg-gray-50">
                            <th className="py-3 px-4 text-left font-semibold text-gray-600 bg-gray-50">Return-Path</th>
                            <td className="py-3 px-4 text-gray-800">{headers.return_path}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default HeaderExplorer;
