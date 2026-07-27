import React, { useState, useEffect } from 'react';

export const ReputationDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await fetch('/api/v1/reputation/analytics/summary');
        if (response.ok) {
          const data = await response.json();
          setAnalytics(data);
        }
      } catch (error) {
        console.error('Failed to fetch reputation analytics', error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <div className="p-8 text-gray-400">Loading Reputation Engine...</div>;

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white flex items-center">
          <svg className="w-8 h-8 mr-3 text-cyan-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          Enterprise Reputation Intelligence Platform
        </h1>
        <p className="text-gray-400 mt-2">Dynamic, evidence-backed scoring (Risk vs. Trust) for all tracked entities.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Profiles Tracked</span>
          <span className="text-4xl font-bold text-white mt-2">{analytics?.total_profiles_tracked?.toLocaleString() || 0}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col relative overflow-hidden">
          <div className="absolute -right-4 -top-4 w-16 h-16 bg-red-500/10 rounded-full blur-xl"></div>
          <span className="text-gray-400 text-sm uppercase tracking-wide">High Risk Entities</span>
          <span className="text-4xl font-bold text-red-400 mt-2">{analytics?.high_risk_entities?.toLocaleString() || 0}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col relative overflow-hidden">
          <div className="absolute -right-4 -top-4 w-16 h-16 bg-orange-500/10 rounded-full blur-xl"></div>
          <span className="text-gray-400 text-sm uppercase tracking-wide">Declining Reputations</span>
          <span className="text-4xl font-bold text-orange-400 mt-2">{analytics?.declining_reputations?.toLocaleString() || 0}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Avg System Trust</span>
          <span className="text-4xl font-bold text-cyan-400 mt-2">{analytics?.average_system_trust || 0}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
           <h3 className="text-lg font-semibold mb-6 text-white flex items-center">
             <svg className="w-5 h-5 mr-2 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
             </svg>
             Top High-Risk Entities
           </h3>
           <div className="space-y-3">
             {/* Mock List */}
             {[
               { id: '192.168.1.45', type: 'IP', risk: 98 },
               { id: 'auth-update-secure.net', type: 'Domain', risk: 95 },
               { id: 'APT29', type: 'Threat Actor', risk: 92 },
             ].map((entity, idx) => (
                <div key={idx} className="flex justify-between items-center p-3 bg-gray-900 rounded border border-gray-700 cursor-pointer hover:border-gray-500">
                  <div>
                    <span className="text-sm font-medium text-gray-200 block">{entity.id}</span>
                    <span className="text-xs text-gray-500">{entity.type}</span>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="text-xs text-gray-400 uppercase">Risk Score</span>
                    <span className="text-lg font-bold text-red-500">{entity.risk}</span>
                  </div>
                </div>
             ))}
           </div>
        </div>

        <div className="bg-gradient-to-br from-cyan-900/30 to-gray-900 p-6 rounded-xl border border-cyan-800/30 flex flex-col">
            <h3 className="text-lg font-semibold text-white flex items-center mb-4">
              <svg className="w-5 h-5 mr-2 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Relationship Influence Engine
            </h3>
            <p className="text-gray-300 text-sm mb-4 flex-grow">
              Reputations are dynamically adjusted based on 1-hop connections in the Knowledge Graph. 
              If a trusted domain resolves to a malicious IP, its Trust Score will automatically decay while its Risk Score increases.
            </p>
            <div className="space-y-2 mt-4 bg-gray-900/50 p-4 rounded border border-cyan-900/50">
              <div className="flex justify-between text-xs text-gray-400">
                <span>KG Sync Status</span>
                <span className="text-green-400">Active</span>
              </div>
              <div className="flex justify-between text-xs text-gray-400">
                <span>Propagation Depth</span>
                <span className="text-cyan-400">1 Hop (Real-time)</span>
              </div>
            </div>
        </div>
      </div>
    </div>
  );
};
