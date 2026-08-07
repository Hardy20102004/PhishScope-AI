import React, { useState, useEffect } from 'react';
import { apiClient as api } from '@/api/client';
import { Database, Clock, RefreshCw, Trash2, Eye } from 'lucide-react';

interface Memory {
  id: string;
  title: string;
  description: string;
  memory_type: string;
  security_classification: string;
  created_at: string;
  confidence_score: number;
}

export const MemoryExplorer: React.FC = () => {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedType, setSelectedType] = useState<string>('');

  const fetchMemories = async () => {
    setLoading(true);
    try {
      const filters = selectedType ? { memory_type: selectedType } : {};
      const res = await api.post('/ai-memory/search', { 
        semantic_search: false, 
        filters,
        limit: 50
      });
      setMemories(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMemories();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedType]);

  const getClassificationColor = (classification: string) => {
    switch (classification) {
      case 'RESTRICTED': return 'text-red-400 border-red-400/30 bg-red-400/10';
      case 'CONFIDENTIAL': return 'text-orange-400 border-orange-400/30 bg-orange-400/10';
      case 'INTERNAL': return 'text-yellow-400 border-yellow-400/30 bg-yellow-400/10';
      default: return 'text-emerald-400 border-emerald-400/30 bg-emerald-400/10';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold text-gray-200 flex items-center gap-2">
          <Database className="w-5 h-5 text-purple-400" />
          Memory Explorer
        </h3>
        <div className="flex gap-2">
          <select 
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="bg-gray-800 border border-gray-700 text-gray-200 text-sm rounded-md px-3 py-1.5 focus:outline-none focus:border-purple-500"
          >
            <option value="">All Types</option>
            <option value="WORKING">Working</option>
            <option value="CASE">Case</option>
            <option value="INVESTIGATION">Investigation</option>
            <option value="THREAT_INTEL">Threat Intel</option>
            <option value="ORGANIZATION">Organization</option>
          </select>
          <button 
            onClick={fetchMemories}
            className="p-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-md transition-colors"
          >
            <RefreshCw className={`w-5 h-5 text-gray-400 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      <div className="bg-gray-900/50 border border-gray-700 rounded-lg overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-800">
            <tr>
              <th className="px-4 py-3 text-xs font-semibold text-gray-400 uppercase">Title</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-400 uppercase">Type</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-400 uppercase">Classification</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-400 uppercase">Confidence</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-400 uppercase">Created</th>
              <th className="px-4 py-3 text-xs font-semibold text-gray-400 uppercase text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {memories.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-4 py-8 text-center text-gray-500">
                  No memories found.
                </td>
              </tr>
            ) : (
              memories.map(mem => (
                <tr key={mem.id} className="hover:bg-gray-800/50 transition-colors">
                  <td className="px-4 py-3">
                    <p className="font-medium text-gray-200">{mem.title}</p>
                    <p className="text-xs text-gray-500 truncate max-w-xs">{mem.description}</p>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-xs font-mono px-2 py-1 bg-gray-800 rounded border border-gray-700 text-gray-300">
                      {mem.memory_type}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`text-[10px] font-bold px-2 py-1 rounded border uppercase ${getClassificationColor(mem.security_classification)}`}>
                      {mem.security_classification}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-1.5 bg-gray-700 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-blue-500" 
                          style={{ width: `${mem.confidence_score * 100}%` }}
                        />
                      </div>
                      <span className="text-xs text-gray-400">{(mem.confidence_score * 100).toFixed(0)}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-xs text-gray-400 flex items-center gap-1 mt-1.5">
                    <Clock className="w-3 h-3" /> {new Date(mem.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button className="text-gray-400 hover:text-white p-1 transition-colors">
                      <Eye className="w-4 h-4" />
                    </button>
                    <button className="text-gray-400 hover:text-red-400 p-1 transition-colors ml-2">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
