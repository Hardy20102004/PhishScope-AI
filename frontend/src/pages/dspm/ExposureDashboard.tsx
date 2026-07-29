import React from 'react';
import { Globe, ShieldAlert, Key } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function ExposureDashboard() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Globe className="text-rose-400" />
                    Data Exposure & Access Governance
                </h2>
                <p className="text-slate-400 mt-1">Identifying public exposures, cross-account sharing, and least-privilege violations on sensitive data.</p>
            </div>
            <div className="flex gap-2">
                <input type="text" placeholder="Search findings..." className="bg-slate-900 border border-slate-700 rounded px-4 py-2 text-sm text-slate-200 w-64 focus:outline-none focus:border-rose-500" />
            </div>
        </div>

        <div className="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden">
            <table className="w-full text-left text-sm">
                <thead className="bg-slate-950/50 border-b border-slate-800 text-slate-400 font-bold uppercase text-xs tracking-wider">
                    <tr>
                        <th className="px-6 py-4">Data Asset</th>
                        <th className="px-6 py-4">Classification</th>
                        <th className="px-6 py-4">Exposure Finding</th>
                        <th className="px-6 py-4">Severity</th>
                        <th className="px-6 py-4">Actions</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                    
                    <ExposureRow 
                        asset="arn:aws:s3:::prod-customer-backups-2026" 
                        classification="PII" 
                        finding="Publicly Readable Bucket Policy (Internet Accessible)" 
                        severity="CRITICAL" 
                    />
                    
                    <ExposureRow 
                        asset="gcp-project/analytics-staging-db" 
                        classification="FINANCIAL" 
                        finding="Cross-Account Sharing (External domain: vendor.com)" 
                        severity="HIGH" 
                    />

                    <ExposureRow 
                        asset="azure-storage/marketing-assets" 
                        classification="PUBLIC" 
                        finding="Public Blob Access Enabled" 
                        severity="LOW" 
                    />

                    <ExposureRow 
                        asset="arn:aws:dynamodb:::session-store" 
                        classification="INTERNAL" 
                        finding="Excessive IAM permissions (14 roles possess full access)" 
                        severity="MEDIUM" 
                    />

                </tbody>
            </table>
        </div>
    </div>
  );
}

function ExposureRow({ asset, classification, finding, severity }: any) {
    let sevStyle = "text-emerald-400 bg-emerald-950/30 border-emerald-900/50";
    if (severity === 'CRITICAL') sevStyle = "text-rose-400 bg-rose-950/30 border-rose-900/50";
    if (severity === 'HIGH') sevStyle = "text-amber-400 bg-amber-950/30 border-amber-900/50";
    if (severity === 'MEDIUM') sevStyle = "text-orange-400 bg-orange-950/30 border-orange-900/50";

    let classStyle = "text-slate-400";
    if (["PII", "PHI", "FINANCIAL"].includes(classification)) classStyle = "text-rose-400 font-bold";

    return (
        <tr className="hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4 font-mono text-xs text-sky-400 max-w-[300px] truncate" title={asset}>
                {asset}
            </td>
            <td className={`px-6 py-4 text-xs tracking-wider ${classStyle}`}>
                {classification}
            </td>
            <td className="px-6 py-4 font-bold text-slate-300">
                <div className="flex items-center gap-2">
                    <ShieldAlert size={16} className="text-slate-500" /> {finding}
                </div>
            </td>
            <td className="px-6 py-4">
                <span className={`text-[10px] font-black tracking-widest px-2 py-1 rounded border ${sevStyle}`}>
                    {severity}
                </span>
            </td>
            <td className="px-6 py-4">
                <Button variant="outline" size="sm" className="border-slate-700 text-slate-300 hover:bg-slate-800 text-xs h-8">
                    Remediate
                </Button>
            </td>
        </tr>
    );
}
