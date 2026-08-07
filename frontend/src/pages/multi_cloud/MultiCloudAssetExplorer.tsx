import React from 'react';
import { Search, Server } from 'lucide-react';

export default function MultiCloudAssetExplorer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Search className="text-sky-400" />
                    Unified Asset Explorer
                </h2>
                <p className="text-slate-400 mt-1">Single pane of glass to search and filter assets across all cloud providers and domains.</p>
            </div>
            <div className="flex gap-2">
                <input type="text" placeholder="Search by ARN, ID, or Name..." className="bg-slate-900 border border-slate-700 rounded px-4 py-2 text-sm text-slate-200 w-80 focus:outline-none focus:border-sky-500" />
            </div>
        </div>

        <div className="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden">
            <table className="w-full text-left text-sm">
                <thead className="bg-slate-950/50 border-b border-slate-800 text-slate-400 font-bold uppercase text-xs tracking-wider">
                    <tr>
                        <th className="px-6 py-4">Asset Name</th>
                        <th className="px-6 py-4">Provider</th>
                        <th className="px-6 py-4">Type / Env</th>
                        <th className="px-6 py-4">Native ID</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                    
                    <AssetRow 
                        name="prod-web-server-01" 
                        provider="AWS" 
                        type="COMPUTE" env="PROD" 
                        nativeId="i-0abcd1234efgh5678" 
                    />
                    
                    <AssetRow 
                        name="analytics-staging-db" 
                        provider="AZURE" 
                        type="STORAGE" env="STAGING" 
                        nativeId="subscriptions/.../analytics-db" 
                    />

                    <AssetRow 
                        name="svc_app_frontend" 
                        provider="AWS" 
                        type="IDENTITY" env="PROD" 
                        nativeId="arn:aws:iam::123456789012:role/svc_app_frontend" 
                    />

                    <AssetRow 
                        name="marketing-campaign-data" 
                        provider="GCP" 
                        type="STORAGE" env="PROD" 
                        nativeId="projects/analytics/datasets/marketing" 
                    />

                </tbody>
            </table>
        </div>
    </div>
  );
}

function AssetRow({ name, provider, type, env, nativeId }: any) {
    let provStyle = "text-amber-500";
    if (provider === 'AZURE') provStyle = "text-blue-500";
    if (provider === 'GCP') provStyle = "text-rose-500";

    return (
        <tr className="hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4 font-bold text-slate-200 flex items-center gap-2">
                <Server size={14} className="text-slate-500" /> {name}
            </td>
            <td className={`px-6 py-4 text-xs font-black tracking-widest ${provStyle}`}>
                {provider}
            </td>
            <td className="px-6 py-4">
                <div className="flex gap-2">
                    <span className="text-[10px] font-bold tracking-widest px-2 py-0.5 rounded border border-slate-700 bg-slate-900 text-slate-400">{type}</span>
                    <span className="text-[10px] font-bold tracking-widest px-2 py-0.5 rounded border border-slate-700 bg-slate-900 text-slate-400">{env}</span>
                </div>
            </td>
            <td className="px-6 py-4 font-mono text-xs text-indigo-400 max-w-[300px] truncate" title={nativeId}>
                {nativeId}
            </td>
        </tr>
    );
}
