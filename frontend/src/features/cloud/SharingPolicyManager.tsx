import React from 'react';

export const SharingPolicyManager: React.FC = () => {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 shadow-lg">
      <h3 className="text-lg font-semibold text-white mb-4 border-b border-gray-700 pb-2">Sharing Policy Engine</h3>
      
      <div className="space-y-4">
         <div className="bg-gray-900 p-4 rounded border border-gray-700">
            <div className="flex justify-between items-center mb-2">
               <span className="font-semibold text-red-500">TLP:RED</span>
               <span className="text-xs bg-gray-800 px-2 py-1 rounded text-gray-400">Default for Workspaces</span>
            </div>
            <p className="text-xs text-gray-500">Not for disclosure, restricted to participants only. Intelligence cannot leave the local workspace.</p>
         </div>

         <div className="bg-gray-900 p-4 rounded border border-gray-700 border-l-2 border-yellow-500">
            <div className="flex justify-between items-center mb-2">
               <span className="font-semibold text-yellow-500">TLP:AMBER</span>
               <span className="text-xs bg-yellow-500/10 px-2 py-1 rounded text-yellow-500 border border-yellow-500/20">Active for Global Exchange</span>
            </div>
            <p className="text-xs text-gray-500">Limited disclosure, restricted to participants' organizations. Intelligence is shared across the Cloud but requires approval workflows.</p>
         </div>

         <div className="bg-gray-900 p-4 rounded border border-gray-700">
            <div className="flex justify-between items-center mb-2">
               <span className="font-semibold text-green-500">TLP:GREEN</span>
            </div>
            <p className="text-xs text-gray-500">Limited disclosure, restricted to the community. Intelligence flows freely to external federated partners (TAXII).</p>
         </div>
      </div>
      
      <div className="mt-6 flex items-center justify-between p-3 bg-gray-900 rounded border border-gray-700">
         <span className="text-sm text-gray-300">Anonymize Source Tenant on Share</span>
         <button className="bg-sky-600 w-10 h-5 rounded-full relative">
            <span className="absolute right-1 top-1 bg-white w-3 h-3 rounded-full"></span>
         </button>
      </div>
    </div>
  );
};
