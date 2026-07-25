import React, { useState } from 'react';
import { apiClient as api } from '@/api/client';
import { Search, BrainCircuit, ShieldAlert } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';

interface SearchResult {
  id: string;
  title: string;
  description: string;
  memory_type: string;
}

export const SemanticSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await api.post('/ai-memory/search', {
        query_text: query,
        semantic_search: true,
        limit: 10
      });
      setResults(res.data);
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
          <BrainCircuit className="w-5 h-5 text-blue-400" />
          Semantic Search Engine
        </h3>
        <p className="text-sm text-gray-400 mt-1">
          Perform high-dimensional vector similarity search across all enterprise memories.
        </p>
      </div>

      <form onSubmit={handleSearch} className="flex gap-3 relative">
        <div className="relative flex-1">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., 'Phishing campaigns targeting HR using malicious PDFs...'"
            className="w-full bg-gray-900 border border-gray-700 text-white rounded-lg pl-12 pr-4 py-3 focus:outline-none focus:border-blue-500 transition-colors"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800/50 disabled:text-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2"
        >
          {loading ? 'Computing Vectors...' : 'Search'}
        </button>
      </form>

      {results.length > 0 && (
        <div className="space-y-4 mt-8">
          <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Top Semantic Matches</h4>
          {results.map((res) => (
            <Card key={res.id} className="bg-gray-800 border-gray-700 hover:border-blue-500/50 transition-colors">
              <CardContent className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <h5 className="font-semibold text-gray-200">{res.title}</h5>
                  <span className="text-[10px] font-mono px-2 py-1 bg-gray-900 rounded border border-gray-700 text-gray-400">
                    {res.memory_type}
                  </span>
                </div>
                <p className="text-sm text-gray-400 line-clamp-3">
                  {res.description}
                </p>
                <div className="mt-4 flex items-center gap-4 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <ShieldAlert className="w-3 h-3 text-orange-400" /> AI Confidence: High
                  </span>
                  <span>ID: {res.id.substring(0, 8)}...</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
