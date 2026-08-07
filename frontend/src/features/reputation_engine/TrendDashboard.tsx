import React from 'react';

export const TrendDashboard: React.FC = () => {
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-semibold text-white mb-6 flex items-center border-b border-gray-700 pb-4">
        <svg className="w-5 h-5 mr-2 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
        </svg>
        Reputation Trend Analysis
      </h3>
      
      <div className="flex items-center justify-center h-64 bg-gray-800 rounded-lg border border-gray-700">
         <div className="text-center">
            <svg className="w-12 h-12 text-gray-600 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <p className="text-gray-400 text-sm">Time-series visualization module ready.</p>
            <p className="text-gray-500 text-xs mt-1">(Integrate Recharts or Chart.js here to plot score history)</p>
         </div>
      </div>
    </div>
  );
};
