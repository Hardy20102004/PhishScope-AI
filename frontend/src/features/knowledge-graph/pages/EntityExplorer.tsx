import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Search, Database, Plus, Trash } from 'lucide-react';
import { apiClient as api } from '@/api/client';

export const EntityExplorer: React.FC = () => {
  const [entities, setEntities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  const fetchEntities = async () => {
    try {
      setLoading(true);
      const res = await api.get('/knowledge-graph/entities');
      setEntities(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    fetchEntities();
  }, []);
  
  return (
    <div className="flex-1 p-8 overflow-y-auto bg-[#0a0a0b] text-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <Database className="w-8 h-8 text-blue-500" />
            Entity Explorer
          </h1>
          <p className="text-gray-400 mt-2">
            Search, filter, and manage individual entities within the knowledge graph.
          </p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors">
          <Plus className="w-5 h-5" />
          Add Entity
        </button>
      </div>

      <Card className="bg-gray-900 border-gray-800">
        <CardContent className="p-0">
          <div className="p-4 border-b border-gray-800 flex justify-between items-center bg-gray-800/30">
            <div className="relative w-72">
              <Search className="w-4 h-4 absolute left-3 top-2.5 text-gray-500" />
              <input
                type="text"
                placeholder="Search entities by name or ID..."
                className="w-full bg-black/50 border border-gray-700 rounded-lg pl-9 pr-4 py-2 text-sm focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-gray-400 uppercase bg-gray-800/50">
                <tr>
                  <th className="px-6 py-3 font-medium">ID</th>
                  <th className="px-6 py-3 font-medium">Type</th>
                  <th className="px-6 py-3 font-medium">Name</th>
                  <th className="px-6 py-3 font-medium">Confidence</th>
                  <th className="px-6 py-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan={5} className="px-6 py-4 text-center text-gray-500">Loading entities...</td></tr>
                ) : entities.length === 0 ? (
                  <tr><td colSpan={5} className="px-6 py-4 text-center text-gray-500">No entities found.</td></tr>
                ) : (
                  entities.map((entity) => (
                    <tr key={entity.id} className="border-b border-gray-800 hover:bg-gray-800/30 transition-colors">
                      <td className="px-6 py-4 font-mono text-xs text-gray-500">{entity.id.substring(0,8)}...</td>
                      <td className="px-6 py-4 font-medium text-gray-300">
                        <span className="bg-gray-800 text-gray-300 px-2 py-1 rounded text-xs border border-gray-700">
                          {entity.entity_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 font-medium text-gray-200">{entity.name}</td>
                      <td className="px-6 py-4">
                        {(entity.confidence * 100).toFixed(0)}%
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button className="text-gray-500 hover:text-red-400 transition-colors">
                          <Trash className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
