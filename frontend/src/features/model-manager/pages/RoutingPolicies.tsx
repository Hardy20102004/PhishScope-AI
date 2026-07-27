import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { GitMerge } from 'lucide-react';
import { apiClient as api } from '@/api/client';

export const RoutingPolicies: React.FC = () => {
  const [policies, setPolicies] = useState([]);

  const fetchPolicies = async () => {
    try {
      const res = await api.get('/models/policies');
      setPolicies(res.data);
    } catch (e) {
      console.error(e);
    }
  };


  useEffect(() => {
    fetchPolicies();
  }, []);

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="mb-8 border-b border-gray-800 pb-6">
        <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
          <GitMerge className="w-8 h-8 text-rose-500" />
          Routing Policies
        </h1>
        <p className="text-gray-400 mt-2">Map task capabilities to primary and fallback models.</p>
      </div>

      <div className="grid gap-4">
        {policies.map((p: any) => (
          <Card key={p.id} className="bg-gray-900 border-gray-800">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">{p.capability}</h3>
                  <div className="flex items-center gap-4 text-sm">
                    <div className="bg-blue-900/20 border border-blue-900/50 px-3 py-1 rounded">
                      <span className="text-gray-500 mr-2">Primary:</span>
                      <span className="text-blue-400 font-medium">{p.primary_model?.name || 'Unassigned'}</span>
                    </div>
                    <div className="bg-gray-800 border border-gray-700 px-3 py-1 rounded">
                      <span className="text-gray-500 mr-2">Fallback:</span>
                      <span className="text-gray-300 font-medium">{p.fallback_model?.name || 'Unassigned'}</span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <span className={`px-2 py-1 text-xs rounded ${p.is_active ? 'bg-emerald-900/50 text-emerald-400' : 'bg-red-900/50 text-red-400'}`}>
                    {p.is_active ? 'ACTIVE' : 'DISABLED'}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
        {policies.length === 0 && <p className="text-gray-500">No routing policies defined.</p>}
      </div>
    </div>
  );
};
