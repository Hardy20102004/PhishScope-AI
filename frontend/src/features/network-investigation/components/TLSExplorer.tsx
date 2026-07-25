import React from 'react';

interface TLSExplorerProps {
    tls: any[];
}

const TLSExplorer: React.FC<TLSExplorerProps> = ({ tls }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">TLS Handshakes</h2>
            
            <div className="overflow-x-auto max-h-[350px]">
                <table className="w-full text-sm text-left text-gray-500">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 sticky top-0">
                        <tr>
                            <th className="px-4 py-3">SNI / Server Name</th>
                            <th className="px-4 py-3">Version</th>
                            <th className="px-4 py-3">Cipher / JA3</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tls.map((record, idx) => (
                            <tr key={idx} className="bg-white border-b hover:bg-gray-50">
                                <td className="px-4 py-3 font-medium text-gray-900 truncate max-w-[150px]">
                                    {record.server_name || '<None>'}
                                </td>
                                <td className="px-4 py-3">
                                    <span className="bg-blue-100 text-blue-800 text-[10px] px-2 py-0.5 rounded font-bold uppercase">
                                        {record.version}
                                    </span>
                                </td>
                                <td className="px-4 py-3 text-xs font-mono text-gray-400">
                                    <div>C: {record.cipher}</div>
                                    {record.ja3_fingerprint && <div className="mt-1">JA3: {record.ja3_fingerprint}</div>}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TLSExplorer;
