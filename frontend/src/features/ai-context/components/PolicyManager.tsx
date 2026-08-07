import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { ShieldCheck, ShieldAlert } from 'lucide-react';
import { apiClient as api } from '@/api/client';

interface Policy {
  id: string;
  name: string;
  policy_type: string;
  is_active: boolean;
}

export const PolicyManager: React.FC = () => {
  const [policies, setPolicies] = useState<Policy[]>([]);

  useEffect(() => {
    const fetchPolicies = async () => {
      try {
        const res = await api.get('/ai-context/policies');
        setPolicies(res.data);
      } catch (err) {
        console.error("Failed to fetch context policies", err);
      }
    };
    fetchPolicies();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-semibold text-gray-200 flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          Context Policy Engine
        </h3>
        <p className="text-sm text-gray-400 mt-1">
          Active rules enforced dynamically before LLM prompt transmission.
        </p>
      </div>

      <div className="grid gap-4">
        {policies.map(policy => (
          <Card key={policy.id} className="bg-gray-800 border-gray-700">
            <CardContent className="p-4 flex items-center justify-between">
              <div className="flex items-center gap-4">
                {policy.is_active ? 
                  <ShieldCheck className="w-6 h-6 text-emerald-400" /> : 
                  <ShieldAlert className="w-6 h-6 text-gray-600" />
                }
                <div>
                  <h4 className="font-semibold text-gray-200">{policy.name}</h4>
                  <p className="text-xs text-gray-500 font-mono mt-1">{policy.policy_type}</p>
                </div>
              </div>
              <div>
                <span className={`text-xs px-2 py-1 rounded border ${policy.is_active ? 'bg-emerald-900/30 border-emerald-800 text-emerald-400' : 'bg-gray-900 border-gray-700 text-gray-500'}`}>
                  {policy.is_active ? 'ENFORCED' : 'DISABLED'}
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
        {policies.length === 0 && (
          <div className="text-gray-500 text-sm italic p-4 bg-gray-900 border border-gray-800 rounded">
            No policies currently configured. The Context Engine will not redact any data.
          </div>
        )}
      </div>
    </div>
  );
};
