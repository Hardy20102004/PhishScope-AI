import React from 'react';

export const FederationDashboard: React.FC = () => {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl shadow-lg p-6">
      <div className="flex justify-between items-center border-b border-gray-700 pb-4 mb-4">
        <h3 className="text-lg font-semibold text-white flex items-center">
          <svg className="w-5 h-5 mr-2 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          Federation Manager (TAXII)
        </h3>
        <button className="bg-green-600 hover:bg-green-500 text-white text-xs px-3 py-1.5 rounded transition-colors shadow">
          Trigger Sync
        </button>
      </div>
      
      <div className="space-y-3">
        <div className="bg-gray-900 p-3 rounded border border-gray-700">
           <div className="flex justify-between items-center">
             <div className="flex items-center">
                <span className="w-2 h-2 rounded-full bg-green-500 mr-2"></span>
                <span className="text-sm font-medium text-gray-200">National CERT Feed</span>
             </div>
             <span className="text-xs text-gray-500">Last Sync: 5 mins ago</span>
           </div>
           <div className="mt-2 flex space-x-4">
             <span className="text-[10px] uppercase text-gray-400 tracking-wider">Type: PULL</span>
             <span className="text-[10px] uppercase text-gray-400 tracking-wider">Protocol: TAXII 2.1</span>
           </div>
        </div>

        <div className="bg-gray-900 p-3 rounded border border-gray-700">
           <div className="flex justify-between items-center">
             <div className="flex items-center">
                <span className="w-2 h-2 rounded-full bg-green-500 mr-2"></span>
                <span className="text-sm font-medium text-gray-200">Industry ISAC Partner</span>
             </div>
             <span className="text-xs text-gray-500">Last Sync: 1 hour ago</span>
           </div>
           <div className="mt-2 flex space-x-4">
             <span className="text-[10px] uppercase text-gray-400 tracking-wider">Type: BI-DIRECTIONAL</span>
             <span className="text-[10px] uppercase text-gray-400 tracking-wider">Protocol: TAXII 2.1</span>
           </div>
        </div>
      </div>
    </div>
  );
};
