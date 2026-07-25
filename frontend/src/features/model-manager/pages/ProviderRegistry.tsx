import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Server, Cpu } from 'lucide-react';
import { apiClient as api } from '@/api/client';

export const ProviderRegistry: React.FC = () => {
  const [providers, setProviders] = useState([]);
  const [models, setModels] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const pRes = await api.get('/models/providers');
      const mRes = await api.get('/models/inventory');
      setProviders(pRes.data);
      setModels(mRes.data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="mb-8 border-b border-gray-800 pb-6">
        <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
          <Server className="w-8 h-8 text-purple-500" />
          Provider & Model Registry
        </h1>
        <p className="text-gray-400 mt-2">Manage connected AI providers and their available models.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-semibold mb-4 text-white">Providers</h2>
          <div className="space-y-4">
            {providers.map((p: any) => (
              <Card key={p.id} className="bg-gray-900 border-gray-800">
                <CardContent className="p-4">
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-bold text-white">{p.name}</h3>
                      <p className="text-xs text-gray-500">{p.base_url || 'Native API'}</p>
                    </div>
                    <span className={`px-2 py-1 text-xs rounded ${p.is_active ? 'bg-emerald-900/50 text-emerald-400' : 'bg-red-900/50 text-red-400'}`}>
                      {p.is_active ? 'ACTIVE' : 'DISABLED'}
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
            {providers.length === 0 && <p className="text-sm text-gray-500">No providers registered.</p>}
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4 text-white">Models Inventory</h2>
          <div className="space-y-4">
            {models.map((m: any) => (
              <Card key={m.id} className="bg-gray-900 border-gray-800">
                <CardContent className="p-4">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-bold text-blue-400 flex items-center gap-2">
                      <Cpu className="w-4 h-4" /> {m.name}
                    </h3>
                    <span className="text-xs text-gray-500">{m.context_window} ctx</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {m.capabilities.map((c: string) => (
                      <span key={c} className="bg-gray-800 text-xs px-2 py-0.5 rounded border border-gray-700 text-gray-300">
                        {c}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
            {models.length === 0 && <p className="text-sm text-gray-500">No models registered.</p>}
          </div>
        </div>
      </div>
    </div>
  );
};
