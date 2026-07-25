import React, { useState } from 'react';
import { ContextExplorer } from '../components/ContextExplorer';
import { TokenAnalytics } from '../components/TokenAnalytics';
import { PolicyManager } from '../components/PolicyManager';
import { FileText, Activity, ShieldCheck } from 'lucide-react';

export const ContextDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'explorer' | 'analytics' | 'policies'>('explorer');

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="mb-8 border-b border-gray-800 pb-6">
        <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
          <FileText className="w-8 h-8 text-purple-500" />
          AI Context Engine
        </h1>
        <p className="text-gray-400 mt-2 max-w-3xl">
          The intelligent bridge optimizing memory retrieval, policy enforcement, and token compression before LLM transmission.
        </p>
      </div>

      <div className="flex gap-4 mb-8">
        <button
          onClick={() => setActiveTab('explorer')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'explorer' ? 'bg-purple-600 text-white' : 'bg-gray-900 text-gray-400 hover:bg-gray-800'
          }`}
        >
          <FileText className="w-4 h-4" /> Context Builder Sandbox
        </button>
        <button
          onClick={() => setActiveTab('analytics')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'analytics' ? 'bg-blue-600 text-white' : 'bg-gray-900 text-gray-400 hover:bg-gray-800'
          }`}
        >
          <Activity className="w-4 h-4" /> Token Analytics
        </button>
        <button
          onClick={() => setActiveTab('policies')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
            activeTab === 'policies' ? 'bg-emerald-600 text-white' : 'bg-gray-900 text-gray-400 hover:bg-gray-800'
          }`}
        >
          <ShieldCheck className="w-4 h-4" /> Policy Engine
        </button>
      </div>

      <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
        {activeTab === 'explorer' && <ContextExplorer />}
        {activeTab === 'analytics' && <TokenAnalytics />}
        {activeTab === 'policies' && <PolicyManager />}
      </div>
    </div>
  );
};
