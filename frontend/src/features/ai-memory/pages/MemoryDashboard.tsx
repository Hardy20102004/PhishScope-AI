import React, { useState } from 'react';
import { MemoryExplorer } from '../components/MemoryExplorer';
import { SemanticSearch } from '../components/SemanticSearch';
import { RelationshipViewer } from '../components/RelationshipViewer';
import { Database, Search, Share2, Activity } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';

export const MemoryDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'explorer' | 'search' | 'graph' | 'analytics'>('explorer');

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="mb-8 border-b border-gray-800 pb-6">
        <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
          <Database className="w-8 h-8 text-blue-500" />
          AI Memory Engine
        </h1>
        <p className="text-gray-400 mt-2 max-w-3xl">
          The persistent, semantic, structured knowledge graph powering PHOENIX X AI agents.
        </p>
      </div>

      <div className="flex gap-4 mb-8">
        <button
          onClick={() => setActiveTab('explorer')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'explorer' ? 'bg-purple-600 text-white' : 'bg-gray-900 text-gray-400 hover:bg-gray-800'
          }`}
        >
          <Database className="w-4 h-4" /> Memory Explorer
        </button>
        <button
          onClick={() => setActiveTab('search')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'search' ? 'bg-blue-600 text-white' : 'bg-gray-900 text-gray-400 hover:bg-gray-800'
          }`}
        >
          <Search className="w-4 h-4" /> Semantic Search
        </button>
        <button
          onClick={() => setActiveTab('graph')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'graph' ? 'bg-emerald-600 text-white' : 'bg-gray-900 text-gray-400 hover:bg-gray-800'
          }`}
        >
          <Share2 className="w-4 h-4" /> Knowledge Graph
        </button>
        <button
          onClick={() => setActiveTab('analytics')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'analytics' ? 'bg-orange-600 text-white' : 'bg-gray-900 text-gray-400 hover:bg-gray-800'
          }`}
        >
          <Activity className="w-4 h-4" /> Engine Analytics
        </button>
      </div>

      <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
        {activeTab === 'explorer' && <MemoryExplorer />}
        {activeTab === 'search' && <SemanticSearch />}
        {activeTab === 'graph' && <RelationshipViewer />}
        {activeTab === 'analytics' && (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <Card className="bg-gray-900 border-gray-800">
              <CardContent className="p-6">
                <p className="text-sm font-medium text-gray-400">Total Memories</p>
                <h3 className="text-3xl font-bold text-white mt-2">1,204</h3>
                <p className="text-xs text-emerald-400 mt-1">+12 in last hour</p>
              </CardContent>
            </Card>
            <Card className="bg-gray-900 border-gray-800">
              <CardContent className="p-6">
                <p className="text-sm font-medium text-gray-400">Graph Edges</p>
                <h3 className="text-3xl font-bold text-white mt-2">3,892</h3>
                <p className="text-xs text-emerald-400 mt-1">Dense clustering detected</p>
              </CardContent>
            </Card>
            <Card className="bg-gray-900 border-gray-800">
              <CardContent className="p-6">
                <p className="text-sm font-medium text-gray-400">Vector Cache Hit Rate</p>
                <h3 className="text-3xl font-bold text-white mt-2">94.2%</h3>
                <p className="text-xs text-emerald-400 mt-1">Highly optimized</p>
              </CardContent>
            </Card>
            <Card className="bg-gray-900 border-gray-800">
              <CardContent className="p-6">
                <p className="text-sm font-medium text-gray-400">Avg Search Latency</p>
                <h3 className="text-3xl font-bold text-white mt-2">42ms</h3>
                <p className="text-xs text-blue-400 mt-1">Hybrid P95</p>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};
