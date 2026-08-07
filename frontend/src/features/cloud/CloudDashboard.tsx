import React, { useState, useEffect } from 'react';

export const CloudDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await fetch('/api/v1/cloud/analytics/summary');
        if (response.ok) {
          const data = await response.json();
          setAnalytics(data);
        }
      } catch (error) {
        console.error('Failed to fetch cloud analytics', error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <div className="p-8 text-gray-400">Loading Cloud Intelligence Manager...</div>;

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white flex items-center">
          <svg className="w-8 h-8 mr-3 text-sky-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
          </svg>
          Enterprise Threat Intelligence Cloud
        </h1>
        <p className="text-gray-400 mt-2">Multi-tenant intelligence management, secure sharing, and TAXII federation.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Active Tenants</span>
          <span className="text-4xl font-bold text-white mt-2">{analytics?.active_tenants || 0}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Workspaces</span>
          <span className="text-4xl font-bold text-sky-400 mt-2">{analytics?.active_workspaces || 0}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Shared Objects</span>
          <span className="text-4xl font-bold text-purple-400 mt-2">{analytics?.shared_objects || 0}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col relative overflow-hidden">
          <div className="absolute -right-4 -top-4 w-16 h-16 bg-green-500/10 rounded-full blur-xl"></div>
          <span className="text-gray-400 text-sm uppercase tracking-wide">Federation Health</span>
          <span className="text-4xl font-bold text-green-400 mt-2">{analytics?.federation_health || 'OFFLINE'}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-gray-800 rounded-xl border border-gray-700 p-6">
           <div className="flex justify-between items-center mb-6">
             <h3 className="text-lg font-semibold text-white">Global Intelligence Exchange</h3>
             <span className="text-xs px-2 py-1 bg-sky-900/50 text-sky-400 border border-sky-800 rounded">TLP:AMBER & Below</span>
           </div>
           
           <div className="space-y-4">
             {[
               { id: 'STIX-1092', type: 'Campaign', tenant: 'Cyber Command', tlp: 'TLP:AMBER', time: '10m ago' },
               { id: 'STIX-1093', type: 'Indicator', tenant: 'SOC Internal', tlp: 'TLP:GREEN', time: '1h ago' },
               { id: 'STIX-1094', type: 'Threat Actor', tenant: 'Partner Org', tlp: 'TLP:CLEAR', time: '3h ago' }
             ].map((item, i) => (
                <div key={i} className="flex items-center justify-between p-3 bg-gray-900 rounded border border-gray-700 hover:border-gray-500 transition-colors cursor-pointer">
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 rounded bg-gray-800 border border-gray-600 flex items-center justify-center">
                       <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                         <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                       </svg>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-200">{item.id} <span className="text-gray-500 text-xs ml-2">({item.type})</span></p>
                      <p className="text-xs text-gray-500 mt-1">Shared by: {item.tenant}</p>
                    </div>
                  </div>
                  <div className="flex flex-col items-end">
                     <span className={`text-xs px-2 py-0.5 rounded font-medium 
                       ${item.tlp === 'TLP:AMBER' ? 'bg-yellow-500/20 text-yellow-500' : 
                         item.tlp === 'TLP:GREEN' ? 'bg-green-500/20 text-green-500' : 
                         'bg-gray-700 text-gray-300'}`}>
                       {item.tlp}
                     </span>
                     <span className="text-[10px] text-gray-500 mt-1">{item.time}</span>
                  </div>
                </div>
             ))}
           </div>
        </div>

        <div className="bg-gradient-to-br from-sky-900/30 to-gray-900 p-6 rounded-xl border border-sky-800/30">
            <h3 className="text-lg font-semibold text-white mb-4">Workspace Manager</h3>
            <p className="text-sm text-gray-300 mb-6">
              Intelligence is physically isolated per Workspace. Data only enters the Global Exchange if a Sharing Policy permits it.
            </p>
            
            <button className="w-full bg-sky-600 hover:bg-sky-500 text-white font-medium py-2 rounded-lg mb-4 transition-colors shadow-lg shadow-sky-900/20">
              Create New Workspace
            </button>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between items-center p-2 bg-gray-800/50 rounded border border-gray-700">
                <span className="text-gray-300">SOC Investigations</span>
                <span className="text-green-400">Active</span>
              </div>
              <div className="flex justify-between items-center p-2 bg-gray-800/50 rounded border border-gray-700">
                <span className="text-gray-300">Threat Hunting Team</span>
                <span className="text-green-400">Active</span>
              </div>
            </div>
        </div>
      </div>
    </div>
  );
};
