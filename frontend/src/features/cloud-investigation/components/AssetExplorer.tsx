import React from 'react';

interface AssetExplorerProps {
    assets: any[];
}

const AssetExplorer: React.FC<AssetExplorerProps> = ({ assets }) => {
    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 h-full">
            <h2 className="text-xl font-semibold mb-4 text-slate-800">Cloud Assets</h2>
            
            <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                {assets.map((asset, idx) => (
                    <div key={idx} className={`p-4 rounded-lg border ${asset.is_public ? 'bg-red-50 border-red-200' : 'bg-slate-50 border-slate-200'}`}>
                        <div className="flex justify-between items-start mb-2">
                            <span className="font-semibold text-slate-900 text-sm truncate pr-2" title={asset.name}>
                                {asset.name}
                            </span>
                            <span className="bg-slate-200 text-slate-800 text-[10px] px-2 py-0.5 rounded font-bold uppercase whitespace-nowrap">
                                {asset.asset_type}
                            </span>
                        </div>
                        <div className="text-xs text-slate-500 mb-2 font-mono truncate" title={asset.asset_id}>
                            {asset.asset_id}
                        </div>
                        <div className="flex justify-between text-xs font-mono text-slate-600 border-t border-slate-200 pt-2 mt-2">
                            <span>{asset.region}</span>
                            {asset.is_public && <span className="text-red-600 font-bold">PUBLIC</span>}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AssetExplorer;
