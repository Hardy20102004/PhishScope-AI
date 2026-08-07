import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Search, Sparkles, ShieldCheck, Database } from 'lucide-react';
import { apiClient as api } from '@/api/client';

export const SearchInterface: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [searchType, setSearchType] = useState('hybrid');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;
    
    setLoading(true);
    try {
      const res = await api.post('/rag/search', {
        query,
        top_k: 5,
        search_type: searchType
      });
      setResults(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 pb-6 border-b border-gray-800">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <Search className="w-8 h-8 text-blue-500" />
            Knowledge Search
          </h1>
          <p className="text-gray-400 mt-2">
            Test the Hybrid Retrieval Engine to visualize semantic ranking and AI citations.
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto space-y-6">
        <form onSubmit={handleSearch} className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search enterprise knowledge..."
            className="w-full bg-gray-900 border border-gray-700 text-white rounded-xl pl-12 pr-32 py-4 text-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 shadow-lg"
          />
          <Search className="w-6 h-6 absolute left-4 top-4 text-gray-500" />
          <div className="absolute right-3 top-3 flex items-center gap-2">
            <select
              value={searchType}
              onChange={(e) => setSearchType(e.target.value)}
              className="bg-gray-800 text-gray-300 border border-gray-700 rounded p-1.5 text-sm focus:outline-none"
            >
              <option value="hybrid">Hybrid</option>
              <option value="vector">Vector Only</option>
              <option value="keyword">Keyword Only</option>
            </select>
            <button
              type="submit"
              disabled={loading || !query}
              className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-lg transition-colors"
            >
              <Sparkles className="w-5 h-5" />
            </button>
          </div>
        </form>

        {loading && (
          <div className="text-center py-12 text-gray-500 flex flex-col items-center">
            <div className="animate-spin mb-4">
              <Database className="w-8 h-8 text-blue-500" />
            </div>
            Executing Hybrid Vector + Keyword Search...
          </div>
        )}

        {results && !loading && (
          <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4">
            <div className="flex justify-between items-center text-sm text-gray-400 px-2">
              <span>Found {results.results.length} evidence chunks</span>
              <span>Latency: {results.latency_ms.toFixed(2)}ms</span>
            </div>
            
            {results.results.map((res: any, idx: number) => (
              <Card key={idx} className="bg-gray-900 border-gray-800 hover:border-gray-700 transition-colors">
                <CardContent className="p-0">
                  <div className="bg-gray-800/50 px-4 py-3 border-b border-gray-800 flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <ShieldCheck className="w-4 h-4 text-emerald-400" />
                      <span className="font-semibold text-gray-200">{res.asset_title}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-gray-500 font-mono">ID: {res.chunk_id.substring(0,8)}...</span>
                      <span className="bg-blue-900/30 text-blue-400 text-xs px-2 py-1 rounded border border-blue-900/50">
                        Score: {(res.score * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                  <div className="p-5 text-gray-300 text-sm leading-relaxed whitespace-pre-wrap font-serif">
                    {res.content}
                  </div>
                </CardContent>
              </Card>
            ))}

            {results.results.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                No matching enterprise knowledge found for this query.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
