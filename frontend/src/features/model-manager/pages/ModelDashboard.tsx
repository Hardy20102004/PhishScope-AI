import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Cpu, Server, Activity, DollarSign } from 'lucide-react';
import { apiClient as api } from '@/api/client';

export const ModelDashboard: React.FC = () => {
  const [summary, setSummary] = useState({ total_cost: 0 });
  const [providers, setProviders] = useState([]);
  const [models, setModels] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [costRes, provRes, modRes] = await Promise.all([
        api.get('/models/costs/summary'),
        api.get('/models/providers'),
        api.get('/models/inventory')
      ]);
      setSummary(costRes.data);
      setProviders(provRes.data);
      setModels(modRes.data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="mb-8 border-b border-gray-800 pb-6">
        <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
          <Cpu className="w-8 h-8 text-blue-500" />
          AI Model Manager
        </h1>
        <p className="text-gray-400 mt-2">Centralized control plane for providers, models, routing, and cost.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-4 mb-8">
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Server className="w-5 h-5 text-purple-400" />
              <p className="text-sm font-medium text-gray-400">Active Providers</p>
            </div>
            <h3 className="text-3xl font-bold text-white">{providers.filter((p:any) => p.is_active).length}</h3>
          </CardContent>
        </Card>
        
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              <p className="text-sm font-medium text-gray-400">Total Models</p>
            </div>
            <h3 className="text-3xl font-bold text-white">{models.length}</h3>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <DollarSign className="w-5 h-5 text-red-400" />
              <p className="text-sm font-medium text-gray-400">Total API Cost</p>
            </div>
            <h3 className="text-3xl font-bold text-white">${summary.total_cost.toFixed(4)}</h3>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
