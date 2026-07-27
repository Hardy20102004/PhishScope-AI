import React, { useState, useEffect } from 'react';

export const AttackGraphDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await fetch('/api/v1/attack-graph/analytics/summary');
        if (response.ok) {
          const data = await response.json();
          setAnalytics(data);
        }
      } catch (error) {
        console.error('Failed to fetch graph analytics', error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <div className="p-8 text-gray-400">Loading Enterprise Attack Graph Engine...</div>;

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center">
            <svg className="w-8 h-8 mr-3 text-fuchsia-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5" />
            </svg>
            Enterprise Attack Graph Generator
          </h1>
          <p className="text-gray-400 mt-2">Interactive visualization and critical path analysis across the Knowledge Graph.</p>
        </div>
        <button className="bg-fuchsia-600 hover:bg-fuchsia-500 text-white px-5 py-2.5 rounded-lg font-medium transition-colors shadow-lg shadow-fuchsia-900/20">
          Build New Graph
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Nodes Tracked</span>
          <span className="text-4xl font-bold text-white mt-2">{analytics?.total_nodes_tracked?.toLocaleString() || 0}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Relationships</span>
          <span className="text-4xl font-bold text-gray-300 mt-2">{analytics?.total_relationships?.toLocaleString() || 0}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col relative overflow-hidden">
          <div className="absolute -right-4 -top-4 w-16 h-16 bg-red-500/10 rounded-full blur-xl"></div>
          <span className="text-gray-400 text-sm uppercase tracking-wide">Critical Paths</span>
          <span className="text-4xl font-bold text-red-400 mt-2">{analytics?.critical_paths_identified || 0}</span>
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow flex flex-col">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Graph Density</span>
          <span className="text-4xl font-bold text-fuchsia-400 mt-2">{analytics?.average_graph_density || 0}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-gray-800 rounded-xl border border-gray-700 p-6">
           <h3 className="text-lg font-semibold text-white mb-4">Recent Graph Snapshots</h3>
           <div className="space-y-3">
             {[1, 2, 3].map(i => (
               <div key={i} className="flex items-center justify-between p-3 bg-gray-900 rounded border border-gray-700 hover:border-gray-500 cursor-pointer transition-colors">
                 <div className="flex items-center">
                   <svg className="w-5 h-5 text-gray-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                   </svg>
                   <div>
                     <p className="text-sm font-medium text-gray-200">APT29 Target Expansion Analysis</p>
                     <p className="text-xs text-gray-500">Seed: Threat Actor (APT29) • Depth: 3</p>
                   </div>
                 </div>
                 <span className="text-xs text-gray-400">2 hours ago</span>
               </div>
             ))}
           </div>
        </div>

        <div className="bg-gradient-to-br from-fuchsia-900/30 to-gray-900 p-6 rounded-xl border border-fuchsia-800/30">
            <h3 className="text-lg font-semibold text-white mb-4">Impact Analysis Engine</h3>
            <p className="text-sm text-gray-300 mb-6">
              The engine continually calculates degree and betweenness centrality to identify high-risk choke points (e.g. shared IPs across campaigns).
            </p>
            <div className="space-y-4">
               <div className="p-3 bg-gray-800/50 rounded border border-gray-700">
                 <div className="flex justify-between text-xs mb-1">
                   <span className="text-gray-300">Centrality Calculation</span>
                   <span className="text-green-400">Online</span>
                 </div>
                 <div className="w-full bg-gray-700 h-1.5 rounded-full"><div className="bg-green-400 h-1.5 rounded-full w-full"></div></div>
               </div>
               <div className="p-3 bg-gray-800/50 rounded border border-gray-700">
                 <div className="flex justify-between text-xs mb-1">
                   <span className="text-gray-300">Community Detection</span>
                   <span className="text-green-400">Online</span>
                 </div>
                 <div className="w-full bg-gray-700 h-1.5 rounded-full"><div className="bg-green-400 h-1.5 rounded-full w-full"></div></div>
               </div>
            </div>
        </div>
      </div>
    </div>
  );
};
