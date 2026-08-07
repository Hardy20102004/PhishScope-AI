import React from 'react';

export const SyncMonitor: React.FC = () => {
  // Mock data for ongoing/recent syncs
  const syncHistory = [
    { id: '1', feed: 'AlienVault OTX', status: 'In Progress', indicators: 450, errors: 0, time: '2 mins ago' },
    { id: '2', feed: 'Internal Honeypot CSV', status: 'Completed', indicators: 1205, errors: 0, time: '1 hour ago' },
    { id: '3', feed: 'STIX Feed Provider A', status: 'Completed with Errors', indicators: 890, errors: 12, time: '3 hours ago' }
  ];

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl shadow-lg p-6 h-full">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold text-white flex items-center">
          <svg className="w-5 h-5 mr-2 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Sync Monitor
        </h3>
        <span className="flex h-3 w-3 relative">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
        </span>
      </div>

      <div className="space-y-4">
        {syncHistory.map((sync) => (
          <div key={sync.id} className="bg-gray-800 rounded-lg p-4 border border-gray-750 flex items-center justify-between">
            <div>
              <h4 className="text-white font-medium">{sync.feed}</h4>
              <div className="flex items-center mt-1 text-xs text-gray-400 space-x-3">
                <span className="flex items-center">
                  <svg className="w-3 h-3 mr-1 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {sync.time}
                </span>
                <span className="flex items-center text-blue-400">
                  <svg className="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                  </svg>
                  {sync.indicators} Indicators
                </span>
                {sync.errors > 0 && (
                  <span className="flex items-center text-red-400">
                    <svg className="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    {sync.errors} Errors
                  </span>
                )}
              </div>
            </div>
            
            <div className={`px-2.5 py-1 rounded text-xs font-medium border
              ${sync.status === 'In Progress' ? 'bg-blue-900/30 text-blue-400 border-blue-800' :
                sync.status === 'Completed' ? 'bg-green-900/30 text-green-400 border-green-800' :
                'bg-yellow-900/30 text-yellow-400 border-yellow-800'
              }`}>
              {sync.status}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
