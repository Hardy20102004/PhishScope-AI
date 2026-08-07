import React from 'react';

interface IdentityExplorerProps {
    identities: any[];
}

const IdentityExplorer: React.FC<IdentityExplorerProps> = ({ identities }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-slate-800">Identities & Permissions</h2>
            
            <div className="overflow-x-auto max-h-[350px]">
                <table className="w-full text-sm text-left text-slate-500">
                    <thead className="text-xs text-slate-700 uppercase bg-slate-50 sticky top-0">
                        <tr>
                            <th className="px-4 py-3">Identity</th>
                            <th className="px-4 py-3">Type</th>
                            <th className="px-4 py-3">Permissions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {identities.map((record, idx) => (
                            <tr key={idx} className={`border-b ${record.is_highly_privileged ? 'bg-orange-50' : 'bg-white hover:bg-slate-50'}`}>
                                <td className="px-4 py-3 font-mono text-xs text-indigo-600 truncate max-w-[150px]" title={record.identity_id}>
                                    {record.name}
                                    {record.is_highly_privileged && <span className="ml-2 bg-orange-600 text-white text-[9px] px-1.5 py-0.5 rounded font-bold uppercase">PRIVILEGED</span>}
                                </td>
                                <td className="px-4 py-3">
                                    <span className="bg-slate-200 text-slate-800 text-[10px] px-2 py-0.5 rounded font-bold uppercase">{record.identity_type}</span>
                                </td>
                                <td className="px-4 py-3 font-mono text-xs">
                                    <div className="flex flex-col gap-1">
                                        {record.permissions.map((p: string, i: number) => (
                                            <span key={i} className="bg-slate-100 px-1 py-0.5 rounded inline-block">{p}</span>
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

export default IdentityExplorer;
