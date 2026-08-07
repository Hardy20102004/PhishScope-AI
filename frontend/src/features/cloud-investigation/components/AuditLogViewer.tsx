import React from 'react';

interface AuditLogViewerProps {
    audits: any[];
}

const AuditLogViewer: React.FC<AuditLogViewerProps> = ({ audits }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-slate-800">Audit Logs (CloudTrail)</h2>
            
            <div className="overflow-x-auto max-h-[350px]">
                <table className="w-full text-sm text-left text-slate-500">
                    <thead className="text-xs text-slate-700 uppercase bg-slate-50 sticky top-0">
                        <tr>
                            <th className="px-4 py-3">Timestamp / IP</th>
                            <th className="px-4 py-3">Actor</th>
                            <th className="px-4 py-3">Event Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {audits.map((record, idx) => (
                            <tr key={idx} className={`border-b ${record.is_anomalous ? 'bg-red-50' : 'bg-white hover:bg-slate-50'}`}>
                                <td className="px-4 py-3 whitespace-nowrap">
                                    <div className="text-xs font-mono">{new Date(record.timestamp).toLocaleString()}</div>
                                    <div className="text-xs text-blue-600 mt-1 font-mono">{record.source_ip}</div>
                                </td>
                                <td className="px-4 py-3 font-semibold text-slate-900 truncate max-w-[150px]" title={record.actor}>
                                    {record.actor}
                                </td>
                                <td className="px-4 py-3">
                                    <div className="font-mono text-xs text-indigo-700 mb-1">{record.event_name}</div>
                                    <div className="text-[10px] text-slate-400 truncate max-w-[150px]">{record.event_source}</div>
                                    {record.is_anomalous && <span className="inline-block mt-1 bg-red-600 text-white text-[9px] px-1.5 py-0.5 rounded font-bold uppercase">ANOMALY</span>}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AuditLogViewer;
