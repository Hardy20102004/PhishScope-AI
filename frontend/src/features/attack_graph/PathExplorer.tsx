import React, { useState, useEffect } from 'react';

export const PathExplorer: React.FC<{ sourceId: string; targetId: string }> = ({ sourceId, targetId }) => {
  const [pathSequence, setPathSequence] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPath = async () => {
      try {
        const response = await fetch(`/api/v1/attack-graph/path?source_id=${sourceId}&target_id=${targetId}`);
        if (response.ok) {
          const data = await response.json();
          setPathSequence(data.path_sequence);
        }
      } catch (error) {
        console.error('Failed to fetch attack path', error);
      } finally {
        setLoading(false);
      }
    };
    fetchPath();
  }, [sourceId, targetId]);

  if (loading) return <div className="p-4 text-gray-400 bg-gray-800 rounded-lg border border-gray-700 animate-pulse h-32 flex items-center justify-center">Calculating Critical Path...</div>;

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl shadow-lg p-5">
      <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
        <svg className="w-5 h-5 mr-2 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        Critical Attack Path
      </h3>

      <div className="relative pl-6 py-2 border-l-2 border-gray-700 space-y-6">
        {pathSequence.map((nodeId, index) => (
          <div key={index} className="relative">
            <div className={`absolute -left-[31px] top-1 w-4 h-4 rounded-full border-2 border-gray-800 
              ${index === 0 ? 'bg-red-500' : index === pathSequence.length - 1 ? 'bg-yellow-500' : 'bg-blue-500'}`}>
            </div>
            <div className="bg-gray-900 border border-gray-700 p-3 rounded shadow-sm flex flex-col hover:border-gray-500 transition-colors cursor-pointer">
              <span className="text-sm font-medium text-white">{nodeId}</span>
              {index === 0 && <span className="text-xs text-red-400 mt-1">Source (Threat Actor)</span>}
              {index === pathSequence.length - 1 && <span className="text-xs text-yellow-400 mt-1">Target (Victim)</span>}
              {index > 0 && index < pathSequence.length - 1 && <span className="text-xs text-blue-400 mt-1">Pivot Node (Infrastructure)</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
