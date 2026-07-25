import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Layers, FileCode, CheckCircle, Activity, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';

interface PromptTemplate {
  id: string;
  name: string;
  category: string;
  description: string;
  is_active: boolean;
}

export const PromptDashboard: React.FC = () => {
  const [templates, setTemplates] = useState<PromptTemplate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        // Mock data for display, in a real scenario this fetches from /api/v1/prompt-platform/
        // Since we didn't hook up a full UI seed script yet, we'll hardcode some for the dashboard UI
        setTemplates([
          { id: '1', name: 'Executive Summary', category: 'Executive Summary', description: 'High-level risk and business impact.', is_active: true },
          { id: '2', name: 'Threat Analysis', category: 'Threat Analysis', description: 'In-depth threat intelligence evaluation.', is_active: true },
          { id: '3', name: 'Incident Report', category: 'Incident Report', description: 'Formal legal-grade regulatory report.', is_active: true }
        ]);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchTemplates();
  }, []);

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <Layers className="w-8 h-8 text-blue-500" />
            Prompt Engineering Platform
          </h1>
          <p className="text-gray-400 mt-2 max-w-3xl">
            Centrally manage, version, and optimize all LLM instructions and templates across PHOENIX X.
          </p>
        </div>
        <Link 
          to="/prompt-platform/editor/new"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Create Prompt
        </Link>
      </div>

      <div className="grid gap-6 md:grid-cols-3 mb-10">
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <FileCode className="w-5 h-5 text-blue-400" />
              <p className="text-sm font-medium text-gray-400">Total Prompts</p>
            </div>
            <h3 className="text-3xl font-bold text-white">42</h3>
            <p className="text-xs text-gray-500 mt-1">Across 12 categories</p>
          </CardContent>
        </Card>
        
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <CheckCircle className="w-5 h-5 text-emerald-400" />
              <p className="text-sm font-medium text-gray-400">Success Rate</p>
            </div>
            <h3 className="text-3xl font-bold text-white">99.2%</h3>
            <p className="text-xs text-emerald-500 mt-1">+0.4% from last week</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="w-5 h-5 text-orange-400" />
              <p className="text-sm font-medium text-gray-400">Avg Latency</p>
            </div>
            <h3 className="text-3xl font-bold text-white">1.2s</h3>
            <p className="text-xs text-orange-500 mt-1">Provider processing time</p>
          </CardContent>
        </Card>
      </div>

      <div className="space-y-4">
        <h3 className="text-xl font-semibold text-gray-200">Active Prompt Library</h3>
        {loading ? (
          <div className="text-gray-500">Loading library...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {templates.map(t => (
              <Card key={t.id} className="bg-gray-800 border-gray-700 hover:border-blue-500/50 transition-colors cursor-pointer group">
                <CardContent className="p-5">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-white group-hover:text-blue-400 transition-colors">{t.name}</h4>
                    <span className="bg-blue-900/30 text-blue-400 text-[10px] px-2 py-0.5 rounded font-medium border border-blue-800/50 uppercase tracking-wider">
                      {t.category}
                    </span>
                  </div>
                  <p className="text-sm text-gray-400 line-clamp-2 mt-2">{t.description}</p>
                  <div className="mt-4 pt-4 border-t border-gray-700 flex justify-between items-center text-xs text-gray-500">
                    <span>v1.2.0 (Published)</span>
                    <span className="flex items-center gap-1 text-emerald-400">
                      <CheckCircle className="w-3 h-3" /> Active
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
