import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Share2, Network, ShieldAlert, Cpu, Activity, Database } from 'lucide-react';
import { Link } from 'react-router-dom';
import { apiClient as api } from '@/api/client';

export const GraphDashboard: React.FC = () => {
  const [centrality, setCentrality] = useState<Record<string, number>>({});
  
  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const res = await api.get('/knowledge-graph/analytics/centrality');
      setCentrality(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <Share2 className="w-8 h-8 text-purple-500" />
            Knowledge Graph Dashboard
          </h1>
          <p className="text-gray-400 mt-2 max-w-3xl">
            Enterprise relationship intelligence layer. Monitor graph growth, inference accuracy, and threat clusters.
          </p>
        </div>
        <div className="flex gap-3">
          <Link 
            to="/knowledge-graph/explore"
            className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors border border-gray-700"
          >
            <Database className="w-5 h-5" />
            Entity Explorer
          </Link>
          <Link 
            to="/knowledge-graph/viewer"
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors"
          >
            <Network className="w-5 h-5" />
            Launch Visualizer
          </Link>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-4 mb-10">
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Cpu className="w-5 h-5 text-blue-400" />
              <p className="text-sm font-medium text-gray-400">Total Entities</p>
            </div>
            <h3 className="text-3xl font-bold text-white">4,892</h3>
            <p className="text-xs text-gray-500 mt-1">Nodes mapped in ontology</p>
          </CardContent>
        </Card>
        
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Share2 className="w-5 h-5 text-purple-400" />
              <p className="text-sm font-medium text-gray-400">Total Relationships</p>
            </div>
            <h3 className="text-3xl font-bold text-white">12,403</h3>
            <p className="text-xs text-gray-500 mt-1">Edges connecting entities</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              <p className="text-sm font-medium text-gray-400">Inference Engine</p>
            </div>
            <h3 className="text-3xl font-bold text-white">1,204</h3>
            <p className="text-xs text-emerald-500 mt-1">Hidden links discovered</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <ShieldAlert className="w-5 h-5 text-orange-400" />
              <p className="text-sm font-medium text-gray-400">Threat Clusters</p>
            </div>
            <h3 className="text-3xl font-bold text-white">18</h3>
            <p className="text-xs text-orange-500 mt-1">Active communities detected</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Highest Centrality Entities</h2>
            <div className="space-y-3">
              {Object.keys(centrality).length === 0 ? (
                <div className="text-gray-500 text-sm py-4">No centrality metrics available.</div>
              ) : (
                Object.entries(centrality).slice(0, 5).map(([id, score]) => (
                  <div key={id} className="flex justify-between items-center p-3 bg-gray-800/50 rounded border border-gray-800">
                    <span className="font-mono text-xs text-gray-300">{id.substring(0,12)}...</span>
                    <span className="bg-purple-900/30 text-purple-400 text-xs px-2 py-1 rounded border border-purple-900/50">
                      Score: {score.toFixed(4)}
                    </span>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
