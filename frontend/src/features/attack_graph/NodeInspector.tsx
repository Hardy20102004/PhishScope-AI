import React, { useState, useEffect } from 'react';

export const NodeInspector: React.FC<{ entityId: string | null }> = ({ entityId }) => {
  const [impact, setImpact] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (entityId) {
      setLoading(true);
      const fetchImpact = async () => {
        try {
          const response = await fetch(`/api/v1/attack-graph/impact/${entityId}`);
          if (response.ok) {
            const data = await response.json();
            setImpact(data);
          }
        } catch (error) {
          console.error('Failed to fetch node impact', error);
        } finally {
          setLoading(false);
        }
      };
      fetchImpact();
    } else {
      setImpact(null);
    }
  }, [entityId]);

  if (!entityId) {
    return (
      <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 h-full flex items-center justify-center text-gray-500 text-sm">
        Select a node in the graph to inspect its details and blast radius.
      </div>
    );
  }

  if (loading) return <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 text-gray-400">Loading Node Details...</div>;

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 shadow-lg">
      <h3 className="text-lg font-semibold text-white mb-4 border-b border-gray-700 pb-2">Node Inspector</h3>
      
      <div className="mb-6">
        <span className="text-xs text-gray-400 uppercase tracking-wide">Selected Entity</span>
        <div className="text-xl font-bold text-gray-100 mt-1">{entityId}</div>
      </div>

      <div className="space-y-4">
        <h4 className="text-sm font-semibold text-gray-300">Impact Analysis</h4>
        
        <div className="bg-gray-900 p-3 rounded border border-gray-700">
          <div className="flex justify-between items-center mb-1">
            <span className="text-xs text-gray-400">Degree Centrality</span>
            <span className="text-xs font-mono text-blue-400">{impact?.degree_centrality || 0}</span>
          </div>
          <p className="text-[10px] text-gray-500">Measures the number of direct connections this node has.</p>
        </div>
        
        <div className="bg-gray-900 p-3 rounded border border-gray-700">
          <div className="flex justify-between items-center mb-1">
            <span className="text-xs text-gray-400">Betweenness Centrality</span>
            <span className="text-xs font-mono text-fuchsia-400">{impact?.betweenness_centrality || 0}</span>
          </div>
          <p className="text-[10px] text-gray-500">Measures how often this node acts as a bridge along the shortest path between two other nodes.</p>
        </div>

        <div className="bg-gray-900 p-3 rounded border border-gray-700 border-l-4 border-l-red-500">
          <div className="flex justify-between items-center mb-1">
            <span className="text-xs text-gray-400 font-semibold">Blast Radius (3 Hops)</span>
            <span className="text-xs font-bold text-red-400">{impact?.blast_radius || 0} Nodes</span>
          </div>
          <p className="text-[10px] text-gray-500">The total number of connected entities that would be affected if this node is compromised or taken offline.</p>
        </div>
      </div>
      
      <button className="w-full mt-6 bg-gray-700 hover:bg-gray-600 text-white text-sm py-2 rounded transition-colors border border-gray-600">
        View Evidence Ledger
      </button>
    </div>
  );
};
