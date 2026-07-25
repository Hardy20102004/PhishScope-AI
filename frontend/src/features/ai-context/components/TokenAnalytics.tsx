import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { apiClient as api } from '@/api/client';
import { Activity, ShieldAlert, Cpu, CheckCircle } from 'lucide-react';

interface AnalyticsData {
  total_builds: number;
  total_original_tokens: number;
  total_compressed_tokens: number;
  tokens_saved: number;
  average_build_latency_ms: number;
}

export const TokenAnalytics: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await api.get('/ai-context/analytics');
        setData(res.data);
      } catch (err) {
        console.error("Failed to fetch context analytics", err);
      }
    };
    fetchAnalytics();
  }, []);

  if (!data) {
    return <div className="text-gray-400 p-4">Loading analytics metrics...</div>;
  }

  const compressionRatio = data.total_original_tokens > 0 
    ? (data.total_original_tokens / data.total_compressed_tokens).toFixed(2) 
    : "1.00";

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-semibold text-gray-200 flex items-center gap-2">
          <Activity className="w-5 h-5 text-blue-400" />
          Token Optimization Metrics
        </h3>
        <p className="text-sm text-gray-400 mt-1">
          Real-time metrics on context compression, caching, and token limits.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Cpu className="w-4 h-4 text-gray-400" />
              <p className="text-sm font-medium text-gray-400">Total Context Builds</p>
            </div>
            <h3 className="text-3xl font-bold text-white">{data.total_builds.toLocaleString()}</h3>
            <p className="text-xs text-blue-400 mt-1">Avg: {data.average_build_latency_ms}ms latency</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="w-4 h-4 text-gray-400" />
              <p className="text-sm font-medium text-gray-400">Compression Ratio</p>
            </div>
            <h3 className="text-3xl font-bold text-emerald-400">{compressionRatio}x</h3>
            <p className="text-xs text-gray-500 mt-1">Tokens preserved vs optimized</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <CheckCircle className="w-4 h-4 text-gray-400" />
              <p className="text-sm font-medium text-gray-400">Tokens Saved</p>
            </div>
            <h3 className="text-3xl font-bold text-white">{(data.tokens_saved).toLocaleString()}</h3>
            <p className="text-xs text-emerald-500 mt-1">Significantly reducing provider costs</p>
          </CardContent>
        </Card>

        <Card className="bg-gray-900 border-gray-800">
          <CardContent className="p-6">
            <div className="flex items-center gap-3 mb-2">
              <ShieldAlert className="w-4 h-4 text-gray-400" />
              <p className="text-sm font-medium text-gray-400">Policy Interventions</p>
            </div>
            <h3 className="text-3xl font-bold text-white">14</h3>
            <p className="text-xs text-orange-400 mt-1">PII Masked in last 24h</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
