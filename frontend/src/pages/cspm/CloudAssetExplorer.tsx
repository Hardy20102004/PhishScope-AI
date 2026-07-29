import React from 'react';
import { Server, Database, Key, Shield, HardDrive, Network } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function CloudAssetExplorer() {
  return (
    <div className="p-8 space-y-6 bg-slate-950 min-h-screen text-slate-100 font-sans border-t border-slate-800">
        
        <div className="flex justify-between items-center border-b border-slate-800 pb-4 mb-6">
            <div>
                <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-200">
                    <Server className="text-sky-400" />
                    Multi-Cloud Asset Explorer
                </h2>
                <p className="text-slate-400 mt-1">Normalized inventory of all discovered cloud resources across AWS, Azure, and GCP.</p>
            </div>
            <div className="flex gap-2">
                <input type="text" placeholder="Search assets (e.g. vpc-production)..." className="bg-slate-900 border border-slate-700 rounded px-4 py-2 text-sm text-slate-200 w-64 focus:outline-none focus:border-sky-500" />
                <Button className="bg-sky-600 hover:bg-sky-700 text-white">Filter</Button>
            </div>
        </div>

        <div className="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden">
            <table className="w-full text-left text-sm">
                <thead className="bg-slate-950/50 border-b border-slate-800 text-slate-400 font-bold uppercase text-xs tracking-wider">
                    <tr>
                        <th className="px-6 py-4">Asset Name</th>
                        <th className="px-6 py-4">Provider</th>
                        <th className="px-6 py-4">Type</th>
                        <th className="px-6 py-4">Region</th>
                        <th className="px-6 py-4">Risk Status</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                    <AssetRow name="prod-db-cluster-01" provider="AWS" type="Database" region="us-east-1" icon={<Database size={16} />} status="SECURE" />
                    <AssetRow name="public-assets-bucket" provider="AWS" type="Storage" region="us-west-2" icon={<HardDrive size={16} />} status="CRITICAL" />
                    <AssetRow name="admin-service-role" provider="Azure" type="Identity" region="global" icon={<Key size={16} />} status="HIGH" />
                    <AssetRow name="frontend-lb-01" provider="GCP" type="Network" region="europe-west1" icon={<Network size={16} />} status="SECURE" />
                    <AssetRow name="waf-global-policy" provider="AWS" type="Security" region="global" icon={<Shield size={16} />} status="SECURE" />
                </tbody>
            </table>
        </div>
    </div>
  );
}

function AssetRow({ name, provider, type, region, icon, status }: any) {
    let statusStyle = "text-emerald-400 bg-emerald-950/30 border-emerald-900/50";
    if (status === 'CRITICAL') statusStyle = "text-rose-400 bg-rose-950/30 border-rose-900/50";
    if (status === 'HIGH') statusStyle = "text-amber-400 bg-amber-950/30 border-amber-900/50";

    return (
        <tr className="hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4 font-bold text-slate-200">
                <div className="flex items-center gap-2">
                    <span className="text-slate-500">{icon}</span> {name}
                </div>
            </td>
            <td className="px-6 py-4 text-slate-400 font-bold">{provider}</td>
            <td className="px-6 py-4 text-slate-400">{type}</td>
            <td className="px-6 py-4 text-slate-400 font-mono text-xs">{region}</td>
            <td className="px-6 py-4">
                <span className={`text-[10px] font-black tracking-widest px-2 py-1 rounded border ${statusStyle}`}>
                    {status}
                </span>
            </td>
        </tr>
    );
}
