import React, { useState, useEffect } from 'react';

interface ThreatActorAnalytics {
  total_actors: number;
  active_campaigns: number;
  average_confidence: number;
  top_targeted_sectors: Record<string, number>;
  emerging_actors: any[];
}

export const ThreatActorDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<ThreatActorAnalytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await fetch('/api/v1/threat-actor/analytics/summary');
        if (response.ok) {
          const data = await response.json();
          setAnalytics(data);
        }
      } catch (error) {
        console.error('Failed to fetch threat actor analytics', error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <div className="p-8 text-gray-400">Loading Threat Actor Intelligence...</div>;

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white flex items-center">
          <svg className="w-8 h-8 mr-3 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Enterprise Threat Actor Intelligence Platform
        </h1>
        <p className="text-gray-400 mt-2">Evidence-backed intelligence profiles, attribution analysis, and MITRE ATT&CK mappings.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Metric Cards */}
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Tracked Profiles</span>
          <span className="text-4xl font-bold text-white mt-2">{analytics?.total_actors}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Active Campaigns</span>
          <span className="text-4xl font-bold text-red-400 mt-2">{analytics?.active_campaigns}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Avg. Attribution Confidence</span>
          <span className="text-4xl font-bold text-blue-400 mt-2">{(analytics?.average_confidence || 0) * 100}%</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
           <h3 className="text-lg font-semibold mb-4 text-white">Top Targeted Sectors</h3>
           <div className="space-y-4 mt-4">
             {Object.entries(analytics?.top_targeted_sectors || {}).map(([sector, count]) => (
                <div key={sector}>
                  <div className="flex justify-between text-sm mb-1 text-gray-300">
                    <span>{sector}</span>
                    <span>{count as React.ReactNode}%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-red-500 h-2 rounded-full" style={{ width: `${count}%` }}></div>
                  </div>
                </div>
             ))}
           </div>
        </div>

        <div className="bg-gradient-to-br from-red-900/40 to-gray-900 p-6 rounded-xl border border-red-800/50 flex flex-col">
            <h3 className="text-lg font-semibold text-white flex items-center mb-4">
              <svg className="w-5 h-5 mr-2 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              AI Attribution Engine
            </h3>
            <p className="text-gray-300 text-sm mb-4 flex-grow">
              The AI Context Engine and Knowledge Graph are continuously evaluating historical overlaps, 
              shared infrastructure, and behavioral similarities to provide explainable attribution confidence.
            </p>
            <button className="bg-red-600 hover:bg-red-500 text-white py-2 px-4 rounded font-medium transition-colors self-start">
              View Attribution Graph
            </button>
        </div>
      </div>
    </div>
  );
};
