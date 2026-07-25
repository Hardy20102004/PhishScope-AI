import React, { useState } from 'react';
import { AgentRegistry } from '../components/AgentRegistry';
import { WorkflowVisualization } from '../components/WorkflowVisualization';
import { ApprovalCenter } from '../components/ApprovalCenter';
import { MemoryViewer } from '../components/MemoryViewer';
import { Brain, GitCommit, UserCheck, Database } from 'lucide-react';

export const AIWorkforceDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'REGISTRY' | 'WORKFLOW' | 'APPROVALS' | 'MEMORY'>('REGISTRY');

  return (
    <div className="p-8 max-w-[1600px] mx-auto min-h-screen bg-gray-950">
      <div className="mb-8 border-b border-gray-800">
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400 tracking-tight mb-2 flex items-center gap-3">
          <Brain className="w-8 h-8 text-purple-500" />
          Enterprise AI Workforce
        </h1>
        <p className="text-gray-400 mb-6">Multi-Agent AI Framework orchestration and monitoring.</p>
        
        <div className="flex space-x-1">
          <button
            onClick={() => setActiveTab('REGISTRY')}
            className={`px-6 py-3 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'REGISTRY' ? 'border-purple-500 text-purple-400' : 'border-transparent text-gray-400 hover:text-gray-300'}`}
          >
            <Brain className="w-4 h-4" /> Agent Registry
          </button>
          <button
            onClick={() => setActiveTab('WORKFLOW')}
            className={`px-6 py-3 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'WORKFLOW' ? 'border-blue-500 text-blue-400' : 'border-transparent text-gray-400 hover:text-gray-300'}`}
          >
            <GitCommit className="w-4 h-4" /> Workflow Engine
          </button>
          <button
            onClick={() => setActiveTab('APPROVALS')}
            className={`px-6 py-3 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'APPROVALS' ? 'border-orange-500 text-orange-400' : 'border-transparent text-gray-400 hover:text-gray-300'}`}
          >
            <UserCheck className="w-4 h-4" /> Approval Center
          </button>
          <button
            onClick={() => setActiveTab('MEMORY')}
            className={`px-6 py-3 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'MEMORY' ? 'border-emerald-500 text-emerald-400' : 'border-transparent text-gray-400 hover:text-gray-300'}`}
          >
            <Database className="w-4 h-4" /> Shared Memory
          </button>
        </div>
      </div>

      <div className="transition-all duration-300">
        {activeTab === 'REGISTRY' && <AgentRegistry />}
        {activeTab === 'WORKFLOW' && <WorkflowVisualization />}
        {activeTab === 'APPROVALS' && <ApprovalCenter />}
        {activeTab === 'MEMORY' && <MemoryViewer />}
      </div>
    </div>
  );
};
