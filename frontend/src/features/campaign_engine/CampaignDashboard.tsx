import React, { useState, useEffect } from 'react';

interface CampaignAnalytics {
  total_campaigns: number;
  active_campaigns: number;
  emerging_clusters: number;
  infrastructure_reuse_rate: number;
  regional_trends: Record<string, number>;
}

export const CampaignDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<CampaignAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [discoveryRunning, setDiscoveryRunning] = useState(false);

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('/api/v1/campaign/analytics/summary');
      if (response.ok) {
        const data = await response.json();
        setAnalytics(data);
      }
    } catch (error) {
      console.error('Failed to fetch campaign analytics', error);
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    fetchAnalytics();
  }, []);

  const handleDiscover = async () => {
    setDiscoveryRunning(true);
    try {
      const response = await fetch('/api/v1/campaign/discover', { method: 'POST' });
      if (response.ok) {
        const result = await response.json();
        alert(`Discovery Complete: Found ${result.clusters_found} clusters, created ${result.new_campaigns_created} emerging campaigns.`);
        fetchAnalytics();
      }
    } catch (error) {
      console.error('Discovery failed', error);
    } finally {
      setDiscoveryRunning(false);
    }
  };

  if (loading) return <div className="p-8 text-gray-400">Loading Campaign Engine...</div>;

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center">
            <svg className="w-8 h-8 mr-3 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
            Campaign Detection Engine
          </h1>
          <p className="text-gray-400 mt-2">AI-driven discovery and clustering of cyber operations.</p>
        </div>
        <button 
          onClick={handleDiscover}
          disabled={discoveryRunning}
          className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white px-5 py-2.5 rounded-lg font-medium transition-colors flex items-center shadow-lg shadow-emerald-900/20"
        >
          {discoveryRunning ? (
            <><span className="animate-spin mr-2">⟳</span> Scanning Graph...</>
          ) : (
            <><svg className="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg> Run AI Discovery</>
          )}
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Tracked Campaigns</span>
          <span className="text-4xl font-bold text-white mt-2">{analytics?.total_campaigns}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col relative overflow-hidden">
          <div className="absolute -right-4 -top-4 w-16 h-16 bg-red-500/10 rounded-full blur-xl"></div>
          <span className="text-gray-400 text-sm uppercase tracking-wide">Active</span>
          <span className="text-4xl font-bold text-red-400 mt-2">{analytics?.active_campaigns}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col relative overflow-hidden">
          <div className="absolute -right-4 -top-4 w-16 h-16 bg-yellow-500/10 rounded-full blur-xl"></div>
          <span className="text-gray-400 text-sm uppercase tracking-wide">Emerging Clusters</span>
          <span className="text-4xl font-bold text-yellow-400 mt-2">{analytics?.emerging_clusters}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Infra Reuse Rate</span>
          <span className="text-4xl font-bold text-emerald-400 mt-2">{(analytics?.infrastructure_reuse_rate || 0) * 100}%</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
           <h3 className="text-lg font-semibold mb-6 text-white flex items-center">
             <svg className="w-5 h-5 mr-2 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
             Targeting Heatmap
           </h3>
           <div className="space-y-4">
             {Object.entries(analytics?.regional_trends || {}).map(([region, count]) => (
                <div key={region}>
                  <div className="flex justify-between text-sm mb-1 text-gray-300">
                    <span>{region}</span>
                    <span className="font-mono text-gray-400">{count as React.ReactNode}%</span>
                  </div>
                  <div className="w-full bg-gray-900 rounded-full h-2">
                    <div className="bg-gradient-to-r from-emerald-500 to-teal-400 h-2 rounded-full" style={{ width: `${count}%` }}></div>
                  </div>
                </div>
             ))}
           </div>
        </div>

        <div className="bg-gradient-to-br from-emerald-900/30 to-gray-900 p-6 rounded-xl border border-emerald-800/30">
            <h3 className="text-lg font-semibold text-white mb-4">Clustering Engine Status</h3>
            <div className="space-y-4">
               <div className="flex items-center justify-between bg-gray-800/50 p-3 rounded">
                 <span className="text-gray-300 text-sm">Knowledge Graph Traversal</span>
                 <span className="px-2 py-0.5 bg-green-500/10 text-green-400 text-xs rounded border border-green-500/20">Optimal</span>
               </div>
               <div className="flex items-center justify-between bg-gray-800/50 p-3 rounded">
                 <span className="text-gray-300 text-sm">Similarity Inference AI</span>
                 <span className="px-2 py-0.5 bg-green-500/10 text-green-400 text-xs rounded border border-green-500/20">Active</span>
               </div>
               <div className="flex items-center justify-between bg-gray-800/50 p-3 rounded">
                 <span className="text-gray-300 text-sm">Auto-Clustering Threshold</span>
                 <span className="px-2 py-0.5 bg-blue-500/10 text-blue-400 text-xs font-mono rounded border border-blue-500/20">&gt; 0.85 Conf.</span>
               </div>
            </div>
        </div>
      </div>
    </div>
  );
};
