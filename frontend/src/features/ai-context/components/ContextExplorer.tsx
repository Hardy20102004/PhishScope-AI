import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Search, FileText, CheckCircle, XCircle } from 'lucide-react';
import { apiClient as api } from '@/api/client';

export const ContextExplorer: React.FC = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleBuild = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    try {
      const res = await api.post('/ai-context/build', {
        query: query,
        max_tokens: 4096,
        apply_compression: true
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-semibold text-gray-200 flex items-center gap-2">
          <FileText className="w-5 h-5 text-purple-400" />
          Context Builder Sandbox
        </h3>
        <p className="text-sm text-gray-400 mt-1">
          Test prompt generation, retrieval, and compression dynamically.
        </p>
      </div>

      <form onSubmit={handleBuild} className="flex gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter query to retrieve and assemble context..."
            className="w-full bg-gray-900 border border-gray-700 text-white rounded-lg pl-12 pr-4 py-3 focus:outline-none focus:border-purple-500 transition-colors"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="bg-purple-600 hover:bg-purple-700 disabled:bg-purple-900/50 disabled:text-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
        >
          {loading ? 'Building...' : 'Build Context'}
        </button>
      </form>

      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          <Card className="lg:col-span-2 bg-gray-900 border-gray-700">
            <CardContent className="p-4">
              <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Final Assembled Context</h4>
              <div className="bg-black/50 border border-gray-800 rounded p-4 h-[400px] overflow-y-auto font-mono text-sm text-gray-300 whitespace-pre-wrap">
                {result.assembled_context}
              </div>
            </CardContent>
          </Card>

          <div className="space-y-4">
            <Card className="bg-gray-900 border-gray-700">
              <CardContent className="p-4">
                <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Validation</h4>
                {result.validation.is_valid ? (
                  <div className="flex items-center gap-2 text-emerald-400 bg-emerald-900/20 p-3 rounded border border-emerald-800/50">
                    <CheckCircle className="w-5 h-5" />
                    <span className="font-medium">Context Passed Policies</span>
                  </div>
                ) : (
                  <div className="flex flex-col gap-2 text-red-400 bg-red-900/20 p-3 rounded border border-red-800/50">
                    <div className="flex items-center gap-2">
                      <XCircle className="w-5 h-5" />
                      <span className="font-medium">Validation Failed</span>
                    </div>
                    <ul className="list-disc list-inside text-xs mt-2">
                      {result.validation.errors.map((e: string, i: number) => <li key={i}>{e}</li>)}
                    </ul>
                  </div>
                )}
                {result.validation.warnings?.length > 0 && (
                  <div className="mt-3 text-orange-400 text-xs p-2 bg-orange-900/10 border border-orange-900/30 rounded">
                    <strong>Warnings:</strong>
                    <ul className="list-disc list-inside mt-1">
                      {result.validation.warnings.map((w: string, i: number) => <li key={i}>{w}</li>)}
                    </ul>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card className="bg-gray-900 border-gray-700">
              <CardContent className="p-4">
                <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Optimization Metrics</h4>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between border-b border-gray-800 pb-2">
                    <span className="text-gray-500">Original Tokens</span>
                    <span className="font-medium text-gray-300">{result.metrics.original_tokens}</span>
                  </div>
                  <div className="flex justify-between border-b border-gray-800 pb-2">
                    <span className="text-gray-500">Compressed Tokens</span>
                    <span className="font-medium text-emerald-400">{result.metrics.compressed_tokens}</span>
                  </div>
                  <div className="flex justify-between border-b border-gray-800 pb-2">
                    <span className="text-gray-500">Latency</span>
                    <span className="font-medium text-blue-400">{result.metrics.build_latency_ms.toFixed(1)} ms</span>
                  </div>
                  <div className="flex justify-between pt-1">
                    <span className="text-gray-500">Cache</span>
                    <span className={`font-medium ${result.metrics.cache_hit ? 'text-emerald-400' : 'text-gray-400'}`}>
                      {result.metrics.cache_hit ? 'HIT' : 'MISS'}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};
