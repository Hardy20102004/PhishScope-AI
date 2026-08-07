import React from 'react';

export const WorkspaceExplorer: React.FC = () => {
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg h-full flex flex-col">
      <div className="p-4 border-b border-gray-700 bg-gray-800 rounded-t-xl flex justify-between items-center">
        <h3 className="text-lg font-semibold text-white flex items-center">
           <svg className="w-5 h-5 mr-2 text-sky-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
           </svg>
           Workspace Explorer
        </h3>
        <select className="bg-gray-900 border border-gray-600 text-gray-300 text-sm rounded px-3 py-1.5 focus:outline-none focus:border-sky-500">
           <option>SOC Investigations (Active)</option>
           <option>Threat Hunting Team</option>
           <option>Malware Research</option>
        </select>
      </div>
      
      <div className="flex-grow p-6">
        <div className="text-center text-gray-500 mt-10">
           <svg className="w-16 h-16 mx-auto mb-4 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 4H6a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-2m-4-1v8m0 0l3-3m-3 3L9 8m-5 5h2.586a1 1 0 01.707.293l2.414 2.414a1 1 0 00.707.293h3.172a1 1 0 00.707-.293l2.414-2.414a1 1 0 01.707-.293H20" />
           </svg>
           <p>This workspace is currently empty.</p>
           <p className="text-sm mt-2">Any intelligence created here is isolated from other tenants.</p>
           <button className="mt-6 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-white px-4 py-2 rounded text-sm transition-colors">
              Import Intelligence
           </button>
        </div>
      </div>
    </div>
  );
};
