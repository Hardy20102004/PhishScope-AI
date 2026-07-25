import React from 'react';

interface DNSExplorerProps {
    dns: any[];
}

const DNSExplorer: React.FC<DNSExplorerProps> = ({ dns }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">DNS Resolution</h2>
            
            <div className="overflow-x-auto max-h-[350px]">
                <table className="w-full text-sm text-left text-gray-500">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 sticky top-0">
                        <tr>
                            <th className="px-4 py-3">Query</th>
                            <th className="px-4 py-3">Type</th>
                            <th className="px-4 py-3">Answers</th>
                        </tr>
                    </thead>
                    <tbody>
                        {dns.map((record, idx) => (
                            <tr key={idx} className={`border-b ${record.is_malicious ? 'bg-red-50' : 'bg-white hover:bg-gray-50'}`}>
                                <td className="px-4 py-3 font-mono text-xs text-indigo-600 truncate max-w-[150px]">
                                    {record.query}
                                    {record.is_malicious && <span className="ml-2 bg-red-600 text-white text-[9px] px-1.5 py-0.5 rounded font-bold uppercase">MALICIOUS</span>}
                                </td>
                                <td className="px-4 py-3">
                                    <span className="bg-gray-200 text-gray-800 text-[10px] px-2 py-0.5 rounded font-bold uppercase">{record.record_type}</span>
                                </td>
                                <td className="px-4 py-3 font-mono text-xs">
                                    <div className="flex flex-col gap-1">
                                        {record.answers.map((ans: string, i: number) => (
                                            <span key={i}>{ans}</span>
                                        ))}
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DNSExplorer;
