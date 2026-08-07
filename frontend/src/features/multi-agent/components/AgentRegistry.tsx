import React, { useEffect, useState } from 'react';
import { apiClient as api } from '@/api/client';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Brain, Activity, Code, Clock } from 'lucide-react';

interface Agent {
  id: string;
  agent_name: string;
  description: string;
  status: string;
  health: string;
  version: string;
  preferred_capability: string;
}

export const AgentRegistry: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await api.get('/multi-agent/agents');
        setAgents(response.data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch agents');
      } finally {
        setLoading(false);
      }
    };
    fetchAgents();
  }, []);

  const handleInitialize = async () => {
    try {
      setLoading(true);
      await api.post('/multi-agent/agents/initialize');
      const response = await api.get('/multi-agent/agents');
      setAgents(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to initialize agents');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-gray-400">Loading AI Workforce...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Brain className="w-6 h-6 text-purple-400" />
            AI Agent Registry
          </h2>
          <p className="text-gray-400 text-sm mt-1">Manage and monitor the enterprise AI workforce.</p>
        </div>
        {agents.length === 0 && (
          <button 
            onClick={handleInitialize}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-md font-medium transition-colors"
          >
            Initialize Workforce
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {agents.map((agent) => (
          <Card key={agent.id} className="bg-gray-800/50 border-gray-700 hover:border-purple-500/50 transition-colors">
            <CardHeader className="pb-2">
              <div className="flex justify-between items-start">
                <CardTitle className="text-lg font-semibold text-gray-100 flex items-center gap-2">
                  {agent.agent_name}
                </CardTitle>
                <Badge variant={agent.status === 'ACTIVE' ? 'success' : 'secondary'}>
                  {agent.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-400 line-clamp-2 mb-4 h-10">
                {agent.description}
              </p>
              
              <div className="space-y-2 text-xs text-gray-300">
                <div className="flex justify-between items-center bg-gray-900/50 p-2 rounded">
                  <span className="flex items-center gap-1"><Activity className="w-3 h-3 text-emerald-400"/> Health</span>
                  <Badge variant={agent.health === 'HEALTHY' ? 'success' : 'destructive'} className="text-[10px] px-1 py-0">
                    {agent.health}
                  </Badge>
                </div>
                
                <div className="flex justify-between items-center bg-gray-900/50 p-2 rounded">
                  <span className="flex items-center gap-1"><Code className="w-3 h-3 text-blue-400"/> Capability</span>
                  <span className="text-gray-400">{agent.preferred_capability || 'General'}</span>
                </div>
                
                <div className="flex justify-between items-center bg-gray-900/50 p-2 rounded">
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3 text-orange-400"/> Version</span>
                  <span className="font-mono">{agent.version}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
        {agents.length === 0 && !loading && (
          <div className="col-span-full py-12 text-center border border-dashed border-gray-700 rounded-lg bg-gray-800/20">
            <Brain className="w-12 h-12 text-gray-600 mx-auto mb-3" />
            <p className="text-gray-400">No agents registered.</p>
            <p className="text-sm text-gray-500 mt-1">Click Initialize Workforce to seed the default agents.</p>
          </div>
        )}
      </div>
    </div>
  );
};
