import React from 'react';

interface ConfigurationViewerProps {
    configs: any[];
}

const ConfigurationViewer: React.FC<ConfigurationViewerProps> = ({ configs }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-slate-800">Configurations</h2>
            
            <div className="overflow-x-auto max-h-[350px]">
                <table className="w-full text-sm text-left text-slate-500">
                    <thead className="text-xs text-slate-700 uppercase bg-slate-50 sticky top-0">
                        <tr>
                            <th className="px-4 py-3">Resource / Type</th>
                            <th className="px-4 py-3">Details</th>
                            <th className="px-4 py-3">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {configs.map((record, idx) => (
                            <tr key={idx} className="bg-white border-b hover:bg-slate-50">
                                <td className="px-4 py-3 whitespace-nowrap">
                                    <div className="font-semibold text-slate-900">{record.resource_id}</div>
                                    <span className="text-[10px] px-2 py-0.5 rounded font-bold uppercase bg-blue-100 text-blue-800 mt-1 inline-block">
                                        {record.config_type}
                                    </span>
                                </td>
                                <td className="px-4 py-3 text-xs font-mono text-slate-500 max-w-[200px]">
                                    <pre className="overflow-x-auto">{JSON.stringify(record.details, null, 2)}</pre>
                                </td>
                                <td className="px-4 py-3">
                                    {record.is_misconfigured ? (
                                        <span className="text-red-600 font-bold text-xs uppercase bg-red-100 px-2 py-1 rounded">Misconfigured</span>
                                    ) : (
                                        <span className="text-green-600 font-bold text-xs uppercase bg-green-100 px-2 py-1 rounded">Secure</span>
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

export default ConfigurationViewer;
